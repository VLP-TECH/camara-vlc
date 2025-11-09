import { useUserProfile } from './useUserProfile';

export const usePermissions = () => {
  const { profile, isAdmin, loading } = useUserProfile();
  
  const isEditor = profile?.role === 'editor';
  const isUser = profile?.role === 'user' || !profile?.role;
  
  // Permisos específicos
  const canExportData = isAdmin || isEditor;
  const canDownloadReports = isAdmin || isEditor;
  const canUploadDataSources = isAdmin || isEditor;
  const canManageUsers = isAdmin;
  const canViewData = isAdmin || profile?.active || false;
  const canAccessAdminPanel = isAdmin;
  
  return {
    profile,
    loading,
    roles: {
      isAdmin,
      isEditor, 
      isUser
    },
    permissions: {
      canExportData,
      canDownloadReports,
      canUploadDataSources,
      canManageUsers,
      canViewData,
      canAccessAdminPanel
    }
  };
};