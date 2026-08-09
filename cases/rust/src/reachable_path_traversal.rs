// RUST-PATH-TRAVERSAL-001 reachable vulnerable fixture. DO NOT DEPLOY.
use std::path::PathBuf;

pub fn resolve_report_path(requested: &str) -> PathBuf {
    PathBuf::from("./reports").join(requested)
}
