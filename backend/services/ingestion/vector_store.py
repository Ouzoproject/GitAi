import hashlib

import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.api.types import Metadata, Embedding

from models import Chunk

BATCH_SIZE = 2000

client = chromadb.PersistentClient(path="./chroma_db")


def collection_name(repo_id: str) -> str:
    """
    Map a repository id ("owner/repo") to a valid Chroma collection name.
    """
    repo_id = repo_id.lower()
    digest = hashlib.sha1(repo_id.encode()).hexdigest()[:8]
    return f"{repo_id.replace('/', '__')}-{digest}"


def get_collection(repo_id: str) -> Collection | None:
    """Return the collection for an indexed repository, or None if not indexed."""
    name = collection_name(repo_id)

    existing = [
        c if isinstance(c, str) else c.name for c in client.list_collections()
    ]
    if name not in existing:
        return None

    return client.get_collection(name)


def store_chunks(
    repo_id: str,
    chunks: list[Chunk],
    embeddings: list[Embedding]
) -> None:
    """
    Store the chunks of one repository in its own collection.

    Re-indexing a repository replaces its previous index; other repositories
    are left untouched.
    """
    name = collection_name(repo_id)

    # Drop any previous index of this repo so chunks never go stale or collide
    if get_collection(repo_id) is not None:
        client.delete_collection(name)

    collection = client.create_collection(
        name=name,
        metadata={"repo": repo_id},
    )

    ids = [chunk.id for chunk in chunks]
    documents = [chunk.text for chunk in chunks]
    metadatas: list[Metadata] = [
        {"source_file": chunk.source_file,
         "chunk_index": chunk.chunk_index}
        for chunk in chunks
    ]

    for i in range(0, len(chunks), BATCH_SIZE):
        collection.add(
            ids=ids[i:i + BATCH_SIZE],
            documents=documents[i:i + BATCH_SIZE],
            embeddings=embeddings[i:i + BATCH_SIZE],
            metadatas=metadatas[i:i + BATCH_SIZE],
        )