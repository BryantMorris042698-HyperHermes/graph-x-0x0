//! Graph_x_0x0 core library
//! Public API for DirectedGraph, RegimeEngine, and metrics.

pub mod graph;
pub mod core;
pub mod orchestrator;

// Re-exports
pub use graph::{DirectedGraph, Node, Edge, GraphSnapshot};
pub use core::RegimeEngine;
pub use orchestrator::Orchestrator;

/// Current version of the high-agent graph engine.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");