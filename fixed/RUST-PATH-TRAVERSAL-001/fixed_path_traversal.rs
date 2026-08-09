// RUST-PATH-TRAVERSAL-001 fixed-version fixture for patch-diff evaluation.
use std::path::{Component, Path, PathBuf};

pub fn resolve_report_path(requested: &str) -> Result<PathBuf, &'static str> {
    let path = Path::new(requested);
    if path.components().any(|part| matches!(part, Component::ParentDir | Component::RootDir | Component::Prefix(_))) {
        return Err("invalid path");
    }
    Ok(PathBuf::from("./reports").join(path))
}
