import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  LinearProgress,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Science as ScienceIcon,
  Assessment as AssessmentIcon,
  Psychology as PsychologyIcon,
  Refresh as RefreshIcon,
  Visibility as ViewIcon,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

interface DashboardStats {
  totalSessions: number;
  activeAgents: number;
  reportsGenerated: number;
  marketValue: number;
}

interface MarketData {
  name: string;
  value: number;
  growth: number;
}

interface AgentStatus {
  name: string;
  status: string;
  queriesProcessed: number;
  avgResponseTime: string;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats>({
    totalSessions: 0,
    activeAgents: 7,
    reportsGenerated: 0,
    marketValue: 0,
  });
  const [marketData, setMarketData] = useState<MarketData[]>([]);
  const [agentStatus, setAgentStatus] = useState<AgentStatus[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading data
    setTimeout(() => {
      setStats({
        totalSessions: 24,
        activeAgents: 7,
        reportsGenerated: 8,
        marketValue: 15200,
      });

      setMarketData([
        { name: 'Breast Cancer', value: 8500, growth: 12.5 },
        { name: 'Ovarian Cancer', value: 3200, growth: 8.3 },
        { name: 'Cervical Cancer', value: 2100, growth: 15.2 },
        { name: 'Endometrial Cancer', value: 1400, growth: 9.7 },
      ]);

      setAgentStatus([
        { name: 'IQVIA Insights', status: 'Active', queriesProcessed: 156, avgResponseTime: '2.1s' },
        { name: 'Patent Landscape', status: 'Active', queriesProcessed: 89, avgResponseTime: '3.2s' },
        { name: 'Clinical Trials', status: 'Active', queriesProcessed: 134, avgResponseTime: '1.8s' },
        { name: 'EXIM Trends', status: 'Active', queriesProcessed: 67, avgResponseTime: '2.5s' },
        { name: 'Web Intelligence', status: 'Active', queriesProcessed: 203, avgResponseTime: '1.2s' },
        { name: 'Internal Knowledge', status: 'Active', queriesProcessed: 45, avgResponseTime: '1.9s' },
        { name: 'Report Generator', status: 'Active', queriesProcessed: 23, avgResponseTime: '4.1s' },
      ]);

      setLoading(false);
    }, 1000);
  }, []);

  const COLORS = ['#1976d2', '#dc004e', '#2e7d32', '#f57c00'];

  const StatCard: React.FC<{ title: string; value: string | number; icon: React.ReactNode; color: string }> = ({
    title,
    value,
    icon,
    color,
  }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box>
            <Typography color="text.secondary" gutterBottom variant="h6">
              {title}
            </Typography>
            <Typography variant="h4" component="div" sx={{ color }}>
              {typeof value === 'number' ? value.toLocaleString() : value}
            </Typography>
          </Box>
          <Box sx={{ color, opacity: 0.8 }}>
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Box sx={{ width: '100%' }}>
        <LinearProgress />
        <Typography sx={{ mt: 2 }}>Loading dashboard...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        PharmaShe Dashboard
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        Welcome to your women's oncology research platform
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Research Sessions"
            value={stats.totalSessions}
            icon={<ScienceIcon sx={{ fontSize: 40 }} />}
            color="primary.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Active Agents"
            value={stats.activeAgents}
            icon={<PsychologyIcon sx={{ fontSize: 40 }} />}
            color="secondary.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Reports Generated"
            value={stats.reportsGenerated}
            icon={<AssessmentIcon sx={{ fontSize: 40 }} />}
            color="success.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Market Value (M$)"
            value={stats.marketValue}
            icon={<TrendingUpIcon sx={{ fontSize: 40 }} />}
            color="warning.main"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Market Analysis Chart */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Women's Oncology Market Analysis
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={marketData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="value" stroke="#1976d2" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
            <CardActions>
              <Button size="small">View Details</Button>
              <Button size="small">Export Data</Button>
            </CardActions>
          </Card>
        </Grid>

        {/* Market Distribution */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Market Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={marketData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {marketData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Agent Status */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  AI Agent Status
                </Typography>
                <IconButton>
                  <RefreshIcon />
                </IconButton>
              </Box>
              <Grid container spacing={2}>
                {agentStatus.map((agent, index) => (
                  <Grid item xs={12} sm={6} md={4} key={index}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                          <Typography variant="subtitle2">{agent.name}</Typography>
                          <Chip
                            label={agent.status}
                            size="small"
                            color={agent.status === 'Active' ? 'success' : 'default'}
                          />
                        </Box>
                        <Typography variant="body2" color="text.secondary">
                          Queries: {agent.queriesProcessed}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Avg Response: {agent.avgResponseTime}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
