// RUST-PATH-TRAVERSAL-001 unreachable/safe paired fixture.
use std::path::{Component, Path, PathBuf};

fn retired_resolve_report_path(requested: &str) -> PathBuf {
    PathBuf::from("./reports").join(requested)
}

pub fn resolve_report_path(requested: &str) -> Result<PathBuf, &'static str> {
    let path = Path::new(requested);
    if path.components().any(|part| matches!(part, Component::ParentDir | Component::RootDir | Component::Prefix(_))) {
        return Err("invalid path");
    }
    Ok(PathBuf::from("./reports").join(path))
}
