-- Sync emails from auth.users to profiles for existing users
UPDATE profiles p
SET email = au.email
FROM auth.users au
WHERE p.user_id = au.id
  AND p.email IS NULL;