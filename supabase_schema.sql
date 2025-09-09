-- Supabase schema for Gita Query chatbot
-- Run this in your Supabase SQL editor

-- Create table for storing verse embeddings
CREATE TABLE IF NOT EXISTS verse_embeddings (
    id SERIAL PRIMARY KEY,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    text TEXT NOT NULL,
    embedding VECTOR(384), -- 384 dimensions for all-MiniLM-L6-v2
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX IF NOT EXISTS verse_embeddings_embedding_idx 
ON verse_embeddings USING ivfflat (embedding vector_cosine_ops);

-- Create table for storing documents
CREATE TABLE IF NOT EXISTS verse_documents (
    id SERIAL PRIMARY KEY,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    text TEXT NOT NULL,
    sanskrit TEXT,
    english TEXT,
    hindi TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create unique constraint
ALTER TABLE verse_documents 
ADD CONSTRAINT unique_chapter_verse UNIQUE (chapter, verse);
