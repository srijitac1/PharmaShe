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
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import {
  Add as AddIcon,
  Download as DownloadIcon,
  Visibility as ViewIcon,
  Delete as DeleteIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';

interface Report {
  id: number;
  title: string;
  report_type: string;
  file_path?: string;
  metadata: any;
  created_at: string;
}

const Reports: React.FC = () => {
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [openDialog, setOpenDialog] = useState(false);
  const [newReport, setNewReport] = useState({
    title: '',
    report_type: 'pdf',
    template: '',
  });

  useEffect(() => {
    // Simulate loading reports
    setTimeout(() => {
      setReports([
        {
          id: 1,
          title: 'Women\'s Oncology Market Analysis',
          report_type: 'pdf',
          file_path: '/reports/market_analysis_20240125.pdf',
          metadata: { pages: 45, charts: 12 },
          created_at: '2024-01-25T10:30:00Z',
        },
        {
          id: 2,
          title: 'Patent Landscape Report',
          report_type: 'excel',
          file_path: '/reports/patent_analysis_20240124.xlsx',
          metadata: { sheets: 5, rows: 1200 },
          created_at: '2024-01-24T14:15:00Z',
        },
        {
          id: 3,
          title: 'Clinical Pipeline Summary',
          report_type: 'pdf',
          file_path: '/reports/clinical_pipeline_20240123.pdf',
          metadata: { pages: 28, charts: 8 },
          created_at: '2024-01-23T09:45:00Z',
        },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleGenerateReport = async () => {
    try {
      const response = await fetch('/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newReport),
      });

      if (response.ok) {
        const report = await response.json();
        setReports(prev => [report, ...prev]);
        setOpenDialog(false);
        setNewReport({ title: '', report_type: 'pdf', template: '' });
      }
    } catch (error) {
      console.error('Error generating report:', error);
    }
  };

  const getReportTypeColor = (type: string) => {
    switch (type) {
      case 'pdf': return 'error';
      case 'excel': return 'success';
      case 'json': return 'info';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Box>
        <Typography>Loading reports...</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Reports</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          Generate Report
        </Button>
      </Box>

      <Grid container spacing={3}>
        {reports.map((report) => (
          <Grid item xs={12} md={6} lg={4} key={report.id}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Typography variant="h6" component="div">
                    {report.title}
                  </Typography>
                  <Chip
                    label={report.report_type.toUpperCase()}
                    size="small"
                    color={getReportTypeColor(report.report_type) as any}
                  />
                </Box>
                
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {report.metadata?.pages && `${report.metadata.pages} pages`}
                  {report.metadata?.sheets && `${report.metadata.sheets} sheets`}
                  {report.metadata?.charts && ` • ${report.metadata.charts} charts`}
                  {report.metadata?.rows && ` • ${report.metadata.rows} rows`}
                </Typography>
                
                <Typography variant="caption" color="text.secondary">
                  Generated: {new Date(report.created_at).toLocaleDateString()}
                </Typography>
              </CardContent>
              
              <CardActions>
                <Button size="small" startIcon={<ViewIcon />}>
                  View
                </Button>
                <Button size="small" startIcon={<DownloadIcon />}>
                  Download
                </Button>
                <IconButton size="small" color="error">
                  <DeleteIcon />
                </IconButton>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Generate Report Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Generate New Report</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Report Title"
              value={newReport.title}
              onChange={(e) => setNewReport(prev => ({ ...prev, title: e.target.value }))}
              sx={{ mb: 2 }}
            />
            
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Report Type</InputLabel>
              <Select
                value={newReport.report_type}
                label="Report Type"
                onChange={(e) => setNewReport(prev => ({ ...prev, report_type: e.target.value }))}
              >
                <MenuItem value="pdf">PDF Report</MenuItem>
                <MenuItem value="excel">Excel Workbook</MenuItem>
                <MenuItem value="json">JSON Data</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl fullWidth>
              <InputLabel>Template</InputLabel>
              <Select
                value={newReport.template}
                label="Template"
                onChange={(e) => setNewReport(prev => ({ ...prev, template: e.target.value }))}
              >
                <MenuItem value="market_analysis">Market Analysis</MenuItem>
                <MenuItem value="patent_landscape">Patent Landscape</MenuItem>
                <MenuItem value="clinical_pipeline">Clinical Pipeline</MenuItem>
                <MenuItem value="comprehensive">Comprehensive Report</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button onClick={handleGenerateReport} variant="contained">
            Generate Report
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Reports;
