import os
import pathlib
from fastmcp import FastMCP

mcp = FastMCP("filesystem-explorer")

@mcp.tool()
def list_directory(path: str) -> dict:
    """List contents of a directory"""
    try:
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            is_dir = os.path.isdir(item_path)
            size = os.path.getsize(item_path) if not is_dir else None
            items.append({
                "name": item,
                "type": "directory" if is_dir else "file",
                "size": size
            })
        return {"path": path, "contents": items}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def read_file(file_path: str, max_lines: int = 100) -> dict:
    """Read contents of a text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:max_lines]
        return {
            "path": file_path,
            "content": "".join(lines),
            "truncated": len(lines) == max_lines
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_files(directory: str, pattern: str, file_type: str = "") -> dict:
    """Search for files by name pattern"""
    import glob
    search_pattern = os.path.join(directory, f"**/*{pattern}*{file_type}")
    matches = glob.glob(search_pattern, recursive=True)
    return {"pattern": pattern, "matches": matches[:50]}  # Limit results

@mcp.tool()
def get_file_info(file_path: str) -> dict:
    """Get detailed file information"""
    try:
        stat = os.stat(file_path)
        return {
            "path": file_path,
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "is_directory": os.path.isdir(file_path),
            "extension": pathlib.Path(file_path).suffix
        }
    except Exception as e:
        return {"error": str(e)}

# Add main block to run as server with different transport options
if __name__ == "__main__":
    # Check for transport type from environment or default to stdio
    transport = os.getenv("FASTMCP_TRANSPORT", "stdio")
    
    if transport == "http" or transport == "streamable-http":
        # Run with HTTP transport for URL-based access
        host = os.getenv("FASTMCP_HOST", "127.0.0.1")
        port = int(os.getenv("FASTMCP_PORT", "8000"))
        print(f"🚀 Starting FastMCP server with HTTP transport on {host}:{port}")
        mcp.run(transport="streamable-http", host=host, port=port)
    else:
        # Default to stdio transport for LangChain integration
        print("🚀 Starting FastMCP server with stdio transport")
        mcp.run()
