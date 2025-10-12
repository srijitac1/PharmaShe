import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Grid,
  LinearProgress,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Psychology as PsychologyIcon,
  Refresh as RefreshIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';

interface Agent {
  name: string;
  description: string;
  status: string;
  queriesProcessed: number;
  avgResponseTime: string;
  lastUpdated: string;
  health: string;
}

const Agents: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [openDialog, setOpenDialog] = useState(false);

  useEffect(() => {
    // Simulate loading agents
    setTimeout(() => {
      setAgents([
        {
          name: 'IQVIA Insights Agent',
          description: 'Provides market trends, sales data, and competitor analysis',
          status: 'active',
          queriesProcessed: 156,
          avgResponseTime: '2.1s',
          lastUpdated: '2024-01-25T14:30:00Z',
          health: 'healthy',
        },
        {
          name: 'Patent Landscape Agent',
          description: 'Monitors global IP filings and analyzes freedom-to-operate risks',
          status: 'active',
          queriesProcessed: 89,
          avgResponseTime: '3.2s',
          lastUpdated: '2024-01-25T14:25:00Z',
          health: 'healthy',
        },
        {
          name: 'Clinical Trials Agent',
          description: 'Monitors clinical development pipeline and trial activity',
          status: 'active',
          queriesProcessed: 134,
          avgResponseTime: '1.8s',
          lastUpdated: '2024-01-25T14:20:00Z',
          health: 'healthy',
        },
        {
          name: 'EXIM Trends Agent',
          description: 'Analyzes global API and formulation trade data',
          status: 'active',
          queriesProcessed: 67,
          avgResponseTime: '2.5s',
          lastUpdated: '2024-01-25T14:15:00Z',
          health: 'healthy',
        },
        {
          name: 'Web Intelligence Agent',
          description: 'Conducts real-time searches across scientific publications',
          status: 'active',
          queriesProcessed: 203,
          avgResponseTime: '1.2s',
          lastUpdated: '2024-01-25T14:10:00Z',
          health: 'healthy',
        },
        {
          name: 'Internal Knowledge Agent',
          description: 'Analyzes internal company documents and historical research',
          status: 'active',
          queriesProcessed: 45,
          avgResponseTime: '1.9s',
          lastUpdated: '2024-01-25T14:05:00Z',
          health: 'healthy',
        },
        {
          name: 'Report Generator Agent',
          description: 'Generates professional PDF and Excel reports',
          status: 'active',
          queriesProcessed: 23,
          avgResponseTime: '4.1s',
          lastUpdated: '2024-01-25T14:00:00Z',
          health: 'healthy',
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'inactive': return 'default';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  const getHealthColor = (health: string) => {
    switch (health) {
      case 'healthy': return 'success';
      case 'warning': return 'warning';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  const handleAgentClick = (agent: Agent) => {
    setSelectedAgent(agent);
    setOpenDialog(true);
  };

  if (loading) {
    return (
      <Box>
        <LinearProgress />
        <Typography sx={{ mt: 2 }}>Loading AI agents...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">AI Agents</Typography>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={() => setLoading(true)}
        >
          Refresh Status
        </Button>
      </Box>

      <Grid container spacing={3}>
        {agents.map((agent, index) => (
          <Grid item xs={12} md={6} lg={4} key={index}>
            <Card 
              sx={{ 
                height: '100%', 
                display: 'flex', 
                flexDirection: 'column',
                cursor: 'pointer',
                '&:hover': {
                  boxShadow: 4,
                },
              }}
              onClick={() => handleAgentClick(agent)}
            >
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <PsychologyIcon sx={{ mr: 1, color: 'primary.main' }} />
                  <Typography variant="h6" component="div">
                    {agent.name}
                  </Typography>
                </Box>
                
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {agent.description}
                </Typography>
                
                <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                  <Chip
                    label={agent.status}
                    size="small"
                    color={getStatusColor(agent.status) as any}
                  />
                  <Chip
                    label={agent.health}
                    size="small"
                    color={getHealthColor(agent.health) as any}
                  />
                </Box>
                
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Queries Processed:
                  </Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {agent.queriesProcessed}
                  </Typography>
                </Box>
                
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Avg Response Time:
                  </Typography>
                  <Typography variant="body2" fontWeight="bold">
                    {agent.avgResponseTime}
                  </Typography>
                </Box>
                
                <Typography variant="caption" color="text.secondary">
                  Last Updated: {new Date(agent.lastUpdated).toLocaleString()}
                </Typography>
              </CardContent>
              
              <CardActions>
                <Button size="small" startIcon={<PlayIcon />}>
                  Test Query
                </Button>
                <IconButton size="small">
                  <SettingsIcon />
                </IconButton>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Agent Details Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedAgent?.name}
        </DialogTitle>
        <DialogContent>
          {selectedAgent && (
            <Box>
              <Typography variant="body1" sx={{ mb: 2 }}>
                {selectedAgent.description}
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Status
                  </Typography>
                  <Chip
                    label={selectedAgent.status}
                    color={getStatusColor(selectedAgent.status) as any}
                  />
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Health
                  </Typography>
                  <Chip
                    label={selectedAgent.health}
                    color={getHealthColor(selectedAgent.health) as any}
                  />
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Queries Processed
                  </Typography>
                  <Typography variant="h6">
                    {selectedAgent.queriesProcessed}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="subtitle2" gutterBottom>
                    Average Response Time
                  </Typography>
                  <Typography variant="h6">
                    {selectedAgent.avgResponseTime}
                  </Typography>
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Close</Button>
          <Button variant="contained">
            Configure Agent
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Agents;
