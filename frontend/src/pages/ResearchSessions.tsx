import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
} from '@mui/material';
import {
  Add as AddIcon,
  Visibility as ViewIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Download as DownloadIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';

interface ResearchSession {
  id: number;
  title: string;
  description?: string;
  query: string;
  status: string;
  created_at: string;
}

const ResearchSessions: React.FC = () => {
  const [sessions, setSessions] = useState<ResearchSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [newSession, setNewSession] = useState({
    title: '',
    description: '',
    query: '',
  });

  useEffect(() => {
    // Simulate loading sessions
    setTimeout(() => {
      setSessions([
        {
          id: 1,
          title: 'Breast Cancer Market Analysis',
          description: 'Comprehensive analysis of breast cancer therapeutics market',
          query: 'Analyze the breast cancer market trends and opportunities',
          status: 'completed',
          created_at: '2024-01-25T10:30:00Z',
        },
        {
          id: 2,
          title: 'Patent Landscape Review',
          description: 'IP analysis for women\'s oncology drugs',
          query: 'Review patent landscape for women\'s cancer treatments',
          status: 'active',
          created_at: '2024-01-24T14:15:00Z',
        },
        {
          id: 3,
          title: 'Clinical Pipeline Assessment',
          description: 'Analysis of ongoing clinical trials',
          query: 'Assess clinical trial pipeline for gynecological cancers',
          status: 'completed',
          created_at: '2024-01-23T09:45:00Z',
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleCreateSession = async () => {
    try {
      const response = await fetch('/api/research/sessions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newSession),
      });

      if (response.ok) {
        const session = await response.json();
        setSessions(prev => [session, ...prev]);
        setOpenDialog(false);
        setNewSession({ title: '', description: '', query: '' });
      }
    } catch (error) {
      console.error('Error creating session:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'primary';
      case 'completed': return 'success';
      case 'archived': return 'default';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Box>
        <Typography>Loading research sessions...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Research Sessions</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          New Session
        </Button>
      </Box>

      <Grid container spacing={3}>
        {sessions.map((session) => (
          <Grid item xs={12} md={6} lg={4} key={session.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Typography variant="h6" component="div">
                    {session.title}
                  </Typography>
                  <Chip
                    label={session.status}
                    size="small"
                    color={getStatusColor(session.status) as any}
                  />
                </Box>
                
                {session.description && (
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    {session.description}
                  </Typography>
                )}
                
                <Typography variant="body2" sx={{ mb: 1 }}>
                  <strong>Query:</strong> {session.query}
                </Typography>
                
                <Typography variant="caption" color="text.secondary">
                  Created: {new Date(session.created_at).toLocaleDateString()}
                </Typography>
              </CardContent>
              
              <CardActions>
                <Button size="small" startIcon={<ViewIcon />}>
                  View
                </Button>
                <Button size="small" startIcon={<DownloadIcon />}>
                  Export
                </Button>
                <IconButton size="small">
                  <EditIcon />
                </IconButton>
                <IconButton size="small" color="error">
                  <DeleteIcon />
                </IconButton>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Create Session Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Research Session</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Session Title"
              value={newSession.title}
              onChange={(e) => setNewSession(prev => ({ ...prev, title: e.target.value }))}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Description"
              multiline
              rows={2}
              value={newSession.description}
              onChange={(e) => setNewSession(prev => ({ ...prev, description: e.target.value }))}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Research Query"
              multiline
              rows={3}
              value={newSession.query}
              onChange={(e) => setNewSession(prev => ({ ...prev, query: e.target.value }))}
              placeholder="Describe what you want to research..."
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleCreateSession} variant="contained">
            Create Session
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ResearchSessions;
