-- Create chatbot_knowledge table to store information from PDFs
CREATE TABLE public.chatbot_knowledge (
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
CREATE INDEX idx_chatbot_knowledge_category ON public.chatbot_knowledge(category);
CREATE INDEX idx_chatbot_knowledge_keywords ON public.chatbot_knowledge USING GIN(keywords);
CREATE INDEX idx_chatbot_knowledge_title ON public.chatbot_knowledge(title);
CREATE INDEX idx_chatbot_knowledge_content_search ON public.chatbot_knowledge USING GIN(to_tsvector('spanish', content));

-- Enable RLS
ALTER TABLE public.chatbot_knowledge ENABLE ROW LEVEL SECURITY;

-- Allow anyone to read chatbot knowledge (public information)
CREATE POLICY "Anyone can view chatbot knowledge"
ON public.chatbot_knowledge
FOR SELECT
USING (true);

-- Only admins can insert/update/delete
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

-- Create trigger for updated_at
CREATE TRIGGER update_chatbot_knowledge_updated_at
BEFORE UPDATE ON public.chatbot_knowledge
FOR EACH ROW
EXECUTE FUNCTION public.update_updated_at_column();

