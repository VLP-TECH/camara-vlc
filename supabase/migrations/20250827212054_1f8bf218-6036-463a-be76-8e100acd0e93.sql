-- Add editor role to the existing role system
-- First, let's see what roles currently exist and add editor as a valid role
-- Since the role column is text type, we just need to document the valid roles

-- Update any existing role constraints or add a check constraint for valid roles
ALTER TABLE public.profiles 
ADD CONSTRAINT valid_roles CHECK (role IN ('user', 'admin', 'editor'));

-- Add comment to document the role system
COMMENT ON COLUMN public.profiles.role IS 'User role: user (default), admin (full access), editor (can upload data sources)';