import React, { useEffect, useState } from 'react';
import { supabase } from '@/integrations/supabase/client';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useToast } from '@/hooks/use-toast';
import { Users, UserCheck, UserX, Shield, Plus, Edit } from 'lucide-react';
import { Navigate } from 'react-router-dom';
import { useUserProfile } from '@/hooks/useUserProfile';
interface Profile {
  id: string;
  user_id: string;
  email: string | null;
  first_name: string | null;
  last_name: string | null;
  organization: string | null;
  role: string;
  active: boolean;
  created_at: string;
}
const AdminDashboard = () => {
  const {
    profile,
    loading,
    isAdmin,
    isActive
  } = useUserProfile();
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [loadingProfiles, setLoadingProfiles] = useState(true);
  const [showCreateUser, setShowCreateUser] = useState(false);
  const [newUser, setNewUser] = useState({
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    organization: '',
    role: 'user'
  });
  const {
    toast
  } = useToast();
  useEffect(() => {
    if (!loading) {
      if (profile && isAdmin && isActive) {
        fetchProfiles();
      } else {
        // Stop loading profiles if user is not admin or not active
        setLoadingProfiles(false);
      }
    }
  }, [profile, isAdmin, isActive, loading]);
  const fetchProfiles = async () => {
    setLoadingProfiles(true);
    const {
      data,
      error
    } = await supabase.from('profiles').select('*').order('created_at', {
      ascending: false
    });
    if (error) {
      toast({
        title: "Error",
        description: "No se pudieron cargar los usuarios",
        variant: "destructive"
      });
      console.error('Error fetching profiles:', error);
    } else {
      setProfiles(data || []);
    }
    setLoadingProfiles(false);
  };
  const toggleUserActive = async (userId: string, currentActive: boolean) => {
    const {
      error
    } = await supabase.from('profiles').update({
      active: !currentActive
    }).eq('user_id', userId);
    if (error) {
      toast({
        title: "Error",
        description: "No se pudo actualizar el estado del usuario",
        variant: "destructive"
      });
      console.error('Error updating user status:', error);
    } else {
      toast({
        title: "Éxito",
        description: `Usuario ${!currentActive ? 'activado' : 'desactivado'} correctamente`
      });
      fetchProfiles();
    }
  };
  const updateUserRole = async (userId: string, newRole: string) => {
    const {
      error
    } = await supabase.from('profiles').update({
      role: newRole
    }).eq('user_id', userId);
    if (error) {
      toast({
        title: "Error",
        description: "No se pudo actualizar el rol del usuario",
        variant: "destructive"
      });
      console.error('Error updating user role:', error);
    } else {
      toast({
        title: "Éxito",
        description: "Rol actualizado correctamente"
      });
      fetchProfiles();
    }
  };
  const createUser = async () => {
    if (!newUser.email || !newUser.password || !newUser.firstName) {
      toast({
        title: "Error",
        description: "Por favor completa todos los campos obligatorios",
        variant: "destructive"
      });
      return;
    }
    try {
      // Create user using Supabase admin API
      const {
        data,
        error
      } = await supabase.auth.signUp({
        email: newUser.email,
        password: newUser.password,
        options: {
          data: {
            first_name: newUser.firstName,
            last_name: newUser.lastName
          }
        }
      });
      if (error) throw error;

      // Update the profile with additional info
      if (data.user) {
        const {
          error: profileError
        } = await supabase.from('profiles').update({
          organization: newUser.organization,
          role: newUser.role,
          active: true
        }).eq('user_id', data.user.id);
        if (profileError) throw profileError;
      }
      toast({
        title: "Éxito",
        description: "Usuario creado correctamente"
      });
      setShowCreateUser(false);
      setNewUser({
        email: '',
        password: '',
        firstName: '',
        lastName: '',
        organization: '',
        role: 'user'
      });
      fetchProfiles();
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.message || "No se pudo crear el usuario",
        variant: "destructive"
      });
      console.error('Error creating user:', error);
    }
  };
  if (loading || loadingProfiles) {
    return <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Cargando dashboard...</p>
        </div>
      </div>;
  }
  if (!profile || !isAdmin || !isActive) {
    return <Navigate to="/" replace />;
  }
  const totalUsers = profiles.length;
  const activeUsers = profiles.filter(p => p.active).length;
  const pendingUsers = profiles.filter(p => !p.active).length;
  const adminUsers = profiles.filter(p => p.role === 'admin').length;
  const editorUsers = profiles.filter(p => p.role === 'editor').length;
  return <div className="min-h-screen bg-background">
      <div className="container mx-auto py-8">
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-foreground mb-2">Dashboard de administración</h1>
              <p className="text-muted-foreground">
                Gestiona usuarios y permisos de acceso al sistema
              </p>
            </div>
            <div className="flex gap-2">
              <Dialog open={showCreateUser} onOpenChange={setShowCreateUser}>
                <DialogTrigger asChild>
                  <Button>
                    <Plus className="h-4 w-4 mr-2" />
                    Crear Usuario
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Crear Nuevo Usuario</DialogTitle>
                  </DialogHeader>
                  <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="grid gap-2">
                        <Label htmlFor="firstName">Nombre *</Label>
                        <Input id="firstName" value={newUser.firstName} onChange={e => setNewUser({
                        ...newUser,
                        firstName: e.target.value
                      })} />
                      </div>
                      <div className="grid gap-2">
                        <Label htmlFor="lastName">Apellidos</Label>
                        <Input id="lastName" value={newUser.lastName} onChange={e => setNewUser({
                        ...newUser,
                        lastName: e.target.value
                      })} />
                      </div>
                    </div>
                    <div className="grid gap-2">
                      <Label htmlFor="email">Email *</Label>
                      <Input id="email" type="email" value={newUser.email} onChange={e => setNewUser({
                      ...newUser,
                      email: e.target.value
                    })} />
                    </div>
                    <div className="grid gap-2">
                      <Label htmlFor="password">Contraseña *</Label>
                      <Input id="password" type="password" value={newUser.password} onChange={e => setNewUser({
                      ...newUser,
                      password: e.target.value
                    })} />
                    </div>
                    <div className="grid gap-2">
                      <Label htmlFor="organization">Organización</Label>
                      <Input id="organization" value={newUser.organization} onChange={e => setNewUser({
                      ...newUser,
                      organization: e.target.value
                    })} />
                    </div>
                    <div className="grid gap-2">
                      <Label htmlFor="role">Rol</Label>
                      <Select value={newUser.role} onValueChange={value => setNewUser({
                      ...newUser,
                      role: value
                    })}>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar rol" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="user">Usuario</SelectItem>
                          <SelectItem value="editor">Editor</SelectItem>
                          <SelectItem value="admin">Administrador</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  <div className="flex justify-end gap-2">
                    <Button variant="outline" onClick={() => setShowCreateUser(false)}>
                      Cancelar
                    </Button>
                    <Button onClick={createUser}>
                      Crear Usuario
                    </Button>
                  </div>
                </DialogContent>
              </Dialog>
            </div>
          </div>
        </div>

        {/* Métricas */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total usuarios</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalUsers}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Usuarios activos</CardTitle>
              <UserCheck className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{activeUsers}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pendientes</CardTitle>
              <UserX className="h-4 w-4 text-orange-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-600">{pendingUsers}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Editores</CardTitle>
              <Edit className="h-4 w-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">{editorUsers}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Administradores</CardTitle>
              <Shield className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">{adminUsers}</div>
            </CardContent>
          </Card>
        </div>

        {/* Tabla de usuarios */}
        <Card>
          <CardHeader>
            <CardTitle>Gestión de usuarios</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Email</TableHead>
                  <TableHead>Nombre</TableHead>
                  <TableHead>Organización</TableHead>
                  <TableHead>Rol</TableHead>
                  <TableHead>Estado</TableHead>
                  <TableHead>Fecha registro</TableHead>
                  <TableHead>Acciones</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {profiles.map(userProfile => <TableRow key={userProfile.id}>
                    <TableCell className="font-medium">
                      {userProfile.email || 'Sin email'}
                    </TableCell>
                    <TableCell>
                      {userProfile.first_name && userProfile.last_name ? `${userProfile.first_name} ${userProfile.last_name}` : 'Sin nombre'}
                    </TableCell>
                    <TableCell>
                      {userProfile.organization || 'No especificada'}
                    </TableCell>
                    <TableCell>
                      <Badge variant={userProfile.role === 'admin' ? 'default' : userProfile.role === 'editor' ? 'outline' : 'secondary'}>
                        {userProfile.role === 'admin' ? 'Administrador' : userProfile.role === 'editor' ? 'Editor' : 'Usuario'}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge variant={userProfile.active ? 'default' : 'destructive'}>
                        {userProfile.active ? 'Activo' : 'Inactivo'}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      {new Date(userProfile.created_at).toLocaleDateString('es-ES')}
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-2">
                        <Button size="sm" variant={userProfile.active ? "destructive" : "default"} onClick={() => toggleUserActive(userProfile.user_id, userProfile.active)} disabled={userProfile.user_id === profile?.user_id}>
                          {userProfile.active ? 'Desactivar' : 'Activar'}
                        </Button>
                        
                        {userProfile.user_id !== profile?.user_id && <Select value={userProfile.role} onValueChange={newRole => updateUserRole(userProfile.user_id, newRole)}>
                            <SelectTrigger className="w-32">
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="user">Usuario</SelectItem>
                              <SelectItem value="editor">Editor</SelectItem>
                              <SelectItem value="admin">Admin</SelectItem>
                            </SelectContent>
                          </Select>}
                      </div>
                    </TableCell>
                  </TableRow>)}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>;
};
export default AdminDashboard;