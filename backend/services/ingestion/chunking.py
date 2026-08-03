
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models import Chunk, SourceFile


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

def chunk_files(files: list[SourceFile]) -> list[Chunk]:
    chunks: list[Chunk] = []

    for file in files:

        texts = splitter.split_text(file.content)

        for index, text in enumerate(texts):

            chunks.append(
                Chunk(
                    id=f"{file.path}_{index}",
                    text=text,
                    source_file=file.path,
                    chunk_index=index,
                )
            )
    print(f"Created {len(chunks)} chunks from {len(files)} files.")

    return chunks