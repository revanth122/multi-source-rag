import os
import glob
import uuid

# A chunk object to store parsed pieces of text
class Chunk:
    def __init__(self, chunk_id, source_type, source_file, text, metadata=None):
        self.id = chunk_id
        self.source_type = source_type
        self.source_file = source_file
        self.text = text
        self.metadata = metadata or {}

    def __repr__(self):
        return f"<Chunk {self.id[:6]} from {self.source_type}>"


# -------------------------
# LOAD & CHUNKING FUNCTIONS
# -------------------------

def load_files(base_path, source_type):
    """Loads all .md and .txt files from a folder and applies chunking."""
    chunks = []

    folder = os.path.join(base_path, source_type)
    print(f"\n[DEBUG] Looking inside folder: {folder}")

    # Print all files detected
    pattern = os.path.join(folder, "*")
    file_list = glob.glob(pattern)
    print("[DEBUG] Files found:", file_list)

    for file_path in file_list:
        # Normalize file extension to lowercase
        ext = os.path.splitext(file_path)[1].lower().strip()

        print("[DEBUG] Checking file:", file_path, "| ext:", ext)

        if ext not in [".md", ".txt"]:
            print("[DEBUG] Skipping (not .md or .txt)")
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw = f.read()
        except Exception as e:
            print(f"[ERROR] Cannot read {file_path}:", e)
            continue

        # Apply the appropriate chunker
        if source_type == "docs":
            print("[DEBUG] Applying docs chunking")
            chunks.extend(chunk_docs(raw, file_path))

        elif source_type == "forums":
            print("[DEBUG] Applying forums chunking")
            chunks.extend(chunk_forums(raw, file_path))

        elif source_type == "blogs":
            print("[DEBUG] Applying blogs chunking")
            chunks.extend(chunk_blogs(raw, file_path))

    print(f"[DEBUG] Total chunks loaded from {source_type}: {len(chunks)}")
    return chunks


# --------- DOCUMENTATION CHUNKING ---------

def chunk_docs(text, file_path):
    """Chunk documentation files by sections and medium text blocks."""
    lines = text.splitlines()
    chunks = []
    buffer = []
    section_title = "Untitled"

    def flush():
        if buffer:
            chunk_text = "\n".join(buffer).strip()
            if chunk_text:
                chunks.append(
                    Chunk(
                        chunk_id=str(uuid.uuid4()),
                        source_type="docs",
                        source_file=file_path,
                        text=chunk_text,
                        metadata={"section": section_title},
                    )
                )
            buffer.clear()

    for line in lines:
        if line.startswith("#"):
            flush()
            section_title = line.strip("# ").strip()
        else:
            buffer.append(line)
            if sum(len(x) for x in buffer) > 1200:  # ~1200 char window
                flush()

    flush()
    return chunks


# --------- FORUM CHUNKING ---------

def chunk_forums(text, file_path):
    """Chunk forum threads split by blank lines (each post is a chunk)."""
    raw_chunks = [blk.strip() for blk in text.split("\n\n") if blk.strip()]
    chunks = []

    for blk in raw_chunks:
        chunks.append(
            Chunk(
                chunk_id=str(uuid.uuid4()),
                source_type="forums",
                source_file=file_path,
                text=blk,
            )
        )

    return chunks


# --------- BLOG CHUNKING ---------

def chunk_blogs(text, file_path):
    """Chunk blogs by sections but with bigger windows."""
    lines = text.splitlines()
    chunks = []
    buffer = []
    section_title = "Untitled"

    def flush():
        if buffer:
            chunk_text = "\n".join(buffer).strip()
            if chunk_text:
                chunks.append(
                    Chunk(
                        chunk_id=str(uuid.uuid4()),
                        source_type="blogs",
                        source_file=file_path,
                        text=chunk_text,
                        metadata={"section": section_title},
                    )
                )
            buffer.clear()

    for line in lines:
        if line.startswith("#"):
            flush()
            section_title = line.strip("# ").strip()
        else:
            buffer.append(line)
            if sum(len(x) for x in buffer) > 1600:  # larger window for blogs
                flush()

    flush()
    return chunks
