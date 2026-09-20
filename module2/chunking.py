def split_text_into_chunks(pages: list[dict], chunk_size: int = 200, chunk_overlap: int = 40) -> list[dict]:
    """
    Splits text from pages into smaller overlapping chunks of words.

    This function processes a list of page dictionaries (from the pdf_parser)
    and segments their text into chunks of a specified size (in word count) with
    a specified overlap. This overlap ensures semantic continuity across chunks,
    which improves Retrieval-Augmented Generation (RAG) performance.

    Args:
        pages (list[dict]): A list of dictionaries representing pages, where
            each dictionary must have keys "page_number" (int) and "text" (str).
        chunk_size (int): The maximum number of words allowed in a single chunk (default is 200).
        chunk_overlap (int): The number of words to overlap between consecutive chunks (default is 40).

    Returns:
        list[dict]: A list of dictionaries representing text chunks. Each dictionary contains:
            - "chunk_index" (int): The sequential index of the chunk in the document.
            - "text" (str): The text content of the chunk.
            - "metadata" (dict): Metadata containing "page_number" (int) of the source page.

    Raises:
        ValueError: If chunk_overlap is greater than or equal to chunk_size.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be strictly less than chunk_size.")

    chunks = []
    global_chunk_index = 0

    # Process each page individually to preserve page-level metadata
    for page in pages:
        page_num = page.get("page_number", 0)
        text = page.get("text", "")
        
        # If the page is empty, skip it
        if not text:
            continue
            
        # Split the page text by whitespace to get individual words
        words = text.split()
        total_words = len(words)
        
        # If the total words on the page are less than or equal to the chunk size,
        # create a single chunk for the entire page.
        if total_words <= chunk_size:
            chunks.append({
                "chunk_index": global_chunk_index,
                "text": " ".join(words),
                "metadata": {
                    "page_number": page_num
                }
            })
            global_chunk_index += 1
            continue

        # Slide a window across the list of words to create chunks
        start_idx = 0
        while start_idx < total_words:
            # Determine the end index of the current chunk
            end_idx = start_idx + chunk_size
            
            # Extract the words for this slice and join them into a string
            chunk_words = words[start_idx:end_idx]
            chunk_text = " ".join(chunk_words)
            
            # Store the chunk with page metadata
            chunks.append({
                "chunk_index": global_chunk_index,
                "text": chunk_text,
                "metadata": {
                    "page_number": page_num
                }
            })
            global_chunk_index += 1
            
            # Advance the start index by step size (chunk_size - chunk_overlap)
            start_idx += (chunk_size - chunk_overlap)

    return chunks
