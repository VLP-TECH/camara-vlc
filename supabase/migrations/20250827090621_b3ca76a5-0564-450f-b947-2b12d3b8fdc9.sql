-- Add active field to profiles table
ALTER TABLE public.profiles 
ADD COLUMN active BOOLEAN DEFAULT false;

-- Create admin dashboard policies
CREATE POLICY "Admins can view all profiles" ON public.profiles
FOR SELECT 
USING (role = 'admin');

CREATE POLICY "Admins can update user status" ON public.profiles
FOR UPDATE 
USING (role = 'admin');

-- Update existing user to be admin (first user becomes admin)
UPDATE public.profiles 
SET role = 'admin', active = true 
WHERE created_at = (SELECT MIN(created_at) FROM public.profiles);

-- Create function to get user role safely
CREATE OR REPLACE FUNCTION public.get_current_user_role()
RETURNS TEXT AS $$
  SELECT role FROM public.profiles WHERE user_id = auth.uid();
$$ LANGUAGE SQL SECURITY DEFINER STABLE;