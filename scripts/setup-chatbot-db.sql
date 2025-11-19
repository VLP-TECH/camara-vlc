-- Script SQL para crear la tabla chatbot_knowledge
-- Ejecuta este script en el SQL Editor de Supabase

-- Create chatbot_knowledge table to store information from PDFs
CREATE TABLE IF NOT EXISTS public.chatbot_knowledge (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  category TEXT NOT NULL, -- 'survey', 'kpi', 'general', etc.
  title TEXT NOT NULL,
  content TEXT NOT NULL, -- Main content/text
  metadata JSONB, -- Additional structured data (KPIs values, survey details, etc.)
  source TEXT, -- Source reference (PDF name, page number, etc.)
  keywords TEXT[], -- Searchable keywords for better matching
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Create indexes for better search performance
CREATE INDEX IF NOT EXISTS idx_chatbot_knowledge_category ON public.chatbot_knowledge(category);
CREATE INDEX IF NOT EXISTS idx_chatbot_knowledge_keywords ON public.chatbot_knowledge USING GIN(keywords);
CREATE INDEX IF NOT EXISTS idx_chatbot_knowledge_title ON public.chatbot_knowledge(title);
CREATE INDEX IF NOT EXISTS idx_chatbot_knowledge_content_search ON public.chatbot_knowledge USING GIN(to_tsvector('spanish', content));

-- Enable RLS
ALTER TABLE public.chatbot_knowledge ENABLE ROW LEVEL SECURITY;

-- Allow anyone to read chatbot knowledge (public information)
DROP POLICY IF EXISTS "Anyone can view chatbot knowledge" ON public.chatbot_knowledge;
CREATE POLICY "Anyone can view chatbot knowledge"
ON public.chatbot_knowledge
FOR SELECT
USING (true);

-- Only admins can insert/update/delete
DROP POLICY IF EXISTS "Admins can manage chatbot knowledge" ON public.chatbot_knowledge;
CREATE POLICY "Admins can manage chatbot knowledge"
ON public.chatbot_knowledge
FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM public.profiles
    WHERE user_id = auth.uid()
    AND role = 'admin'
  )
);

-- Create trigger for updated_at (if function doesn't exist, create it first)
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
DROP TRIGGER IF EXISTS update_chatbot_knowledge_updated_at ON public.chatbot_knowledge;
CREATE TRIGGER update_chatbot_knowledge_updated_at
BEFORE UPDATE ON public.chatbot_knowledge
FOR EACH ROW
EXECUTE FUNCTION public.update_updated_at_column();

