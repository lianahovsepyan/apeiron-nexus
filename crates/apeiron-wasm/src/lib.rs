use apeiron_math::{validate_density, ComplexDecimal, Matrix};
use serde::Deserialize;
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn engine_version() -> String {
    "69.0.0-exact-rational".to_string()
}

#[wasm_bindgen]
pub fn status_vocabulary() -> String {
    "PASS,FAIL,BOUNDARY,SKIPPED,VERIFICATION_DISAGREEMENT,ERROR,INCOMPLETE".to_string()
}

#[derive(Deserialize)]
struct MatrixPayload {
    dimension: usize,
    entries: Vec<ComplexDecimal>,
}

#[wasm_bindgen]
pub fn verify_density_matrix_json(payload_json: &str) -> String {
    let parsed: Result<MatrixPayload, _> = serde_json::from_str(payload_json);
    let payload = match parsed {
        Ok(p) => p,
        Err(e) => return format!(r#"{{"error":"Invalid matrix JSON: {}"}}"#, e),
    };

    let mat = match Matrix::from_decimal(payload.dimension, payload.dimension, &payload.entries) {
        Ok(m) => m,
        Err(e) => return format!(r#"{{"error":"Math error: {}"}}"#, e),
    };

    match validate_density(&mat) {
        Ok(checks) => serde_json::to_string(&checks).unwrap_or_else(|e| format!(r#"{{"error":"{}"}}"#, e)),
        Err(e) => format!(r#"{{"error":"Verification failed: {}"}}"#, e),
    }
}
