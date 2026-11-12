use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use serde::{Deserialize, Serialize};
use thiserror::Error;

pub type Rational = BigRational;

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum MathError {
    #[error("invalid finite decimal: {0}")]
    InvalidDecimal(String),
    #[error("decimal exponent exceeds limit")]
    ExponentLimit,
    #[error("matrix must be non-empty and rectangular")]
    MatrixShape,
    #[error("matrix must be square")]
    NotSquare,
    #[error("matrix dimensions are incompatible")]
    DimensionMismatch,
    #[error("matrix is not Hermitian")]
    NotHermitian,
    #[error("matrix is not positive semidefinite")]
    NotPositiveSemidefinite,
}

pub fn parse_decimal(s: &str) -> Result<Rational, MathError> {
    if s.is_empty() || s.trim() != s || s.len() > 256 {
        return Err(MathError::InvalidDecimal(s.into()));
    }
    let (negative, body) = if let Some(x) = s.strip_prefix('-') {
        (true, x)
    } else if let Some(x) = s.strip_prefix('+') {
        (false, x)
    } else {
        (false, s)
    };
    if body.is_empty() {
        return Err(MathError::InvalidDecimal(s.into()));
    }
    let mut parts = body.split(['e', 'E']);
    let mant = parts.next().unwrap();
    let exp_s = parts.next();
    if parts.next().is_some() {
        return Err(MathError::InvalidDecimal(s.into()));
    }
    let mut split = mant.split('.');
    let whole = split.next().unwrap();
    let frac = split.next().unwrap_or("");
    if split.next().is_some()
        || mant.ends_with('.')
        || whole.is_empty()
        || !whole.bytes().all(|b| b.is_ascii_digit())
        || !frac.bytes().all(|b| b.is_ascii_digit())
    {
        return Err(MathError::InvalidDecimal(s.into()));
    }
    let exp: i32 = match exp_s {
        None => 0,
        Some(x) => x.parse().map_err(|_| MathError::ExponentLimit)?,
    };
    if exp.unsigned_abs() > 10000 || frac.len() > 10000 {
        return Err(MathError::ExponentLimit);
    }
    let digits = format!("{whole}{frac}");
    let mut n = BigInt::parse_bytes(digits.as_bytes(), 10)
        .ok_or_else(|| MathError::InvalidDecimal(s.into()))?;
    if negative {
        n = -n;
    }
    let scale = (frac.len() as i32)
        .checked_sub(exp)
        .ok_or(MathError::ExponentLimit)?;
    if scale >= 0 {
        let den = BigInt::from(10u8).pow(scale as u32);
        Ok(Rational::new(n, den))
    } else {
        Ok(Rational::from_integer(
            n * BigInt::from(10u8).pow((-scale) as u32),
        ))
    }
}

pub fn rational_string(x: &Rational) -> String {
    if x.denom().is_one() {
        x.numer().to_string()
    } else {
        format!("{}/{}", x.numer(), x.denom())
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ComplexDecimal {
    pub re: String,
    pub im: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Cx {
    pub re: Rational,
    pub im: Rational,
}

impl Cx {
    pub fn zero() -> Self {
        Self { re: Rational::zero(), im: Rational::zero() }
    }
    pub fn one() -> Self {
        Self { re: Rational::one(), im: Rational::zero() }
    }
    pub fn from_dec(x: &ComplexDecimal) -> Result<Self, MathError> {
        Ok(Self { re: parse_decimal(&x.re)?, im: parse_decimal(&x.im)? })
    }
    pub fn conj(&self) -> Self {
        Self { re: self.re.clone(), im: -self.im.clone() }
    }
    pub fn add(&self, b: &Self) -> Self {
        Self { re: &self.re + &b.re, im: &self.im + &b.im }
    }
    pub fn sub(&self, b: &Self) -> Self {
        Self { re: &self.re - &b.re, im: &self.im - &b.im }
    }
    pub fn mul(&self, b: &Self) -> Self {
        Self {
            re: &self.re * &b.re - &self.im * &b.im,
            im: &self.re * &b.im + &self.im * &b.re,
        }
    }
    pub fn div_real(&self, d: &Rational) -> Self {
        Self { re: &self.re / d, im: &self.im / d }
    }
    pub fn is_zero(&self) -> bool {
        self.re.is_zero() && self.im.is_zero()
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Matrix {
    pub rows: usize,
    pub cols: usize,
    pub data: Vec<Cx>,
}

impl Matrix {
    pub fn new(rows: usize, cols: usize, data: Vec<Cx>) -> Result<Self, MathError> {
        if rows == 0 || cols == 0 || rows.checked_mul(cols) != Some(data.len()) {
            return Err(MathError::MatrixShape);
        }
        Ok(Self { rows, cols, data })
    }
    pub fn zeros(r: usize, c: usize) -> Self {
        Self { rows: r, cols: c, data: vec![Cx::zero(); r * c] }
    }
    pub fn from_decimal(r: usize, c: usize, x: &[ComplexDecimal]) -> Result<Self, MathError> {
        Self::new(r, c, x.iter().map(Cx::from_dec).collect::<Result<Vec<_>, _>>()?)
    }
    pub fn is_hermitian(&self) -> bool {
        if self.rows != self.cols {
            return false;
        }
        for i in 0..self.rows {
            for j in 0..self.cols {
                if self[(i, j)] != self[(j, i)].conj() {
                    return false;
                }
            }
        }
        true
    }
    pub fn trace(&self) -> Result<Cx, MathError> {
        if self.rows != self.cols {
            return Err(MathError::NotSquare);
        }
        let mut t = Cx::zero();
        for i in 0..self.rows {
            t = t.add(&self[(i, i)]);
        }
        Ok(t)
    }
    pub fn psd_witness(&self) -> Result<PsdWitness, MathError> {
        if self.rows != self.cols {
            return Err(MathError::NotSquare);
        }
        if !self.is_hermitian() {
            return Err(MathError::NotHermitian);
        }
        let n = self.rows;
        let mut a = self.clone();
        let mut pivots = Vec::with_capacity(n);
        for k in 0..n {
            let p = a[(k, k)].re.clone();
            if !a[(k, k)].im.is_zero() {
                return Err(MathError::NotHermitian);
            }
            if p.is_negative() {
                return Err(MathError::NotPositiveSemidefinite);
            }
            pivots.push(rational_string(&p));
            if p.is_zero() {
                for i in k + 1..n {
                    if !a[(i, k)].is_zero() {
                        return Err(MathError::NotPositiveSemidefinite);
                    }
                }
                continue;
            }
            for i in k + 1..n {
                for j in k + 1..n {
                    let correction = a[(i, k)].mul(&a[(k, j)]).div_real(&p);
                    a[(i, j)] = a[(i, j)].sub(&correction);
                }
            }
            for i in k + 1..n {
                a[(i, k)] = Cx::zero();
                a[(k, i)] = Cx::zero();
            }
        }
        Ok(PsdWitness { dimension: n, pivots })
    }
}

impl std::ops::Index<(usize, usize)> for Matrix {
    type Output = Cx;
    fn index(&self, (i, j): (usize, usize)) -> &Cx {
        &self.data[i * self.cols + j]
    }
}
impl std::ops::IndexMut<(usize, usize)> for Matrix {
    fn index_mut(&mut self, (i, j): (usize, usize)) -> &mut Cx {
        &mut self.data[i * self.cols + j]
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct PsdWitness {
    pub dimension: usize,
    pub pivots: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CheckResult {
    pub predicate: String,
    pub passed: bool,
    pub evidence: String,
}

pub fn validate_density(rho: &Matrix) -> Result<Vec<CheckResult>, MathError> {
    if rho.rows != rho.cols {
        return Err(MathError::NotSquare);
    }
    let witness = rho.psd_witness()?;
    let tr = rho.trace()?;
    let trace_ok = tr.re == Rational::one() && tr.im.is_zero();
    Ok(vec![
        CheckResult {
            predicate: "HERMITICITY".into(),
            passed: true,
            evidence: "exact conjugate symmetry".into(),
        },
        CheckResult {
            predicate: "POSITIVE_SEMIDEFINITE".into(),
            passed: true,
            evidence: serde_json::to_string(&witness).unwrap(),
        },
        CheckResult {
            predicate: "UNIT_TRACE".into(),
            passed: trace_ok,
            evidence: rational_string(&tr.re),
        },
    ])
}
