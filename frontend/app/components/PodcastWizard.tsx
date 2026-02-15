"use client"
import React, { useState, useEffect, useRef } from 'react';
import {
  Box, Stepper, Step, StepLabel, Button, Typography,
  TextField, Slider, Select, MenuItem, FormControl, InputLabel,
  Card, CardContent, CardActions, Checkbox, FormGroup, FormControlLabel,
  LinearProgress, Paper, Grid, Chip, Stack, Alert,
  Dialog, DialogTitle, DialogContent, DialogActions
} from '@mui/material';
import { useRouter } from 'next/navigation';
import { Mic, AutoAwesome, Description, Settings, Add, Person } from '@mui/icons-material';

// Interfaces
interface Agent {
  id: string;
  name: string;
  role: string;
  personality: string;
  voice_id: string;
}

interface ScriptOutline {
  duration: number;
  topics_to_approach: string[];
  topics_to_avoid: string[];
  questions: string[];
  roles: string[] | Record<string, any>;
}

const steps = ['Configuration', 'Research & Script', 'Review', 'Studio'];
const GOOGLE_VOICES = ["Puck", "Charley", "Aoede", "Fenrir", "Kore"];

export default function PodcastWizard() {
  const [activeStep, setActiveStep] = useState(0);
  const [agents, setAgents] = useState<Agent[]>([]);

  // Config State
  const [theme, setTheme] = useState('');
  const [duration, setDuration] = useState(15);
  const [tone, setTone] = useState('engaging');
  const [selectedAgentIds, setSelectedAgentIds] = useState<string[]>([]);

  // Agent Creation State
  const [openAgentModal, setOpenAgentModal] = useState(false);
  const [newAgent, setNewAgent] = useState({ name: '', role: 'Guest', personality: '', voice_id: 'Puck' });

  // Generation State
  const [isGenerating, setIsGenerating] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [progress, setProgress] = useState(0);
  const [scriptOutline, setScriptOutline] = useState<ScriptOutline | null>(null);
  const logsEndRef = useRef<HTMLDivElement>(null);

  const router = useRouter();

  const fetchAgents = () => {
    fetch('http://localhost:8000/api/agents')
      .then(res => res.json())
      .then(data => setAgents(data))
      .catch(err => console.error("Failed to fetch agents", err));
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  // Scroll logs
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  const handleNext = () => setActiveStep((prev) => prev + 1);
  const handleBack = () => setActiveStep((prev) => prev - 1);

  const handleCreateAgent = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newAgent)
      });
      if (res.ok) {
        setOpenAgentModal(false);
        fetchAgents();
        setNewAgent({ name: '', role: 'Guest', personality: '', voice_id: 'Puck' });
      }
    } catch (err) {
      console.error(err);
    }
  };

  const startGeneration = async () => {
    setIsGenerating(true);
    setLogs(["Starting process..."]);
    setProgress(0);
    handleNext(); // Move to Step 1 (Research & Script)

    try {
      const response = await fetch('http://localhost:8000/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          theme,
          duration,
          tone,
          agent_ids: selectedAgentIds
        })
      });

      if (!response.body) throw new Error("No response body");
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (!line.trim()) continue;
          try {
            const event = JSON.parse(line);
            if (event.type === 'log') {
              setLogs(prev => [...prev, `[LOG] ${event.message}`]);
            } else if (event.type === 'progress') {
              setProgress(event.percent);
            } else if (event.type === 'result') {
              setScriptOutline(event.data);
              setLogs(prev => [...prev, "[SUCCESS] Script generated successfully!"]);
            } else if (event.type === 'error') {
               setLogs(prev => [...prev, `[ERROR] ${event.message}`]);
            }
          } catch (e) {
            console.error("Failed to parse stream line", line, e);
          }
        }
      }
    } catch (err) {
      console.error(err);
      setLogs(prev => [...prev, `[FATAL ERROR] ${err}`]);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleEnterStudio = () => {
    const roomName = theme.replace(/\s+/g, '-').toLowerCase() || 'studio-1';
    router.push(`/room/${roomName}`);
  };

  const renderConfig = () => (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>Podcast Settings</Typography>
      <Grid container spacing={3}>
        <Grid size={12}>
          <TextField
            fullWidth label="Podcast Theme" variant="outlined"
            value={theme} onChange={(e) => setTheme(e.target.value)}
            helperText="What is this episode about?"
          />
        </Grid>
        <Grid size={6}>
           <Typography gutterBottom>Duration: {duration} min</Typography>
           <Slider
             value={duration}
             onChange={(_, val) => setDuration(val as number)}
             min={5} max={60} step={5} marks
             valueLabelDisplay="auto"
           />
        </Grid>
        <Grid size={6}>
          <FormControl fullWidth>
            <InputLabel>Tone</InputLabel>
            <Select value={tone} label="Tone" onChange={(e) => setTone(e.target.value)}>
              <MenuItem value="engaging">Engaging</MenuItem>
              <MenuItem value="serious">Serious</MenuItem>
              <MenuItem value="humorous">Humorous</MenuItem>
              <MenuItem value="educational">Educational</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      <Box sx={{ mt: 6, mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h6">Select Agents</Typography>
        <Button startIcon={<Add />} onClick={() => setOpenAgentModal(true)}>
          Add Agent
        </Button>
      </Box>

      <Grid container spacing={2}>
        {agents.map(agent => (
          <Grid size={{ xs: 12, sm: 4 }} key={agent.id}>
            <Card variant={selectedAgentIds.includes(agent.id) ? "outlined" : "elevation"}
                  sx={{
                    border: selectedAgentIds.includes(agent.id) ? '2px solid #90caf9' : '1px solid #333',
                    cursor: 'pointer',
                    bgcolor: 'background.paper'
                  }}
                  onClick={() => {
                    setSelectedAgentIds(prev =>
                      prev.includes(agent.id) ? prev.filter(id => id !== agent.id) : [...prev, agent.id]
                    );
                  }}
            >
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Person fontSize="small" color="primary" />
                  <Typography variant="h6">{agent.name}</Typography>
                </Box>
                <Chip label={agent.role} size="small" sx={{ mb: 1, mr: 1 }} />
                <Chip label={agent.voice_id} size="small" variant="outlined" sx={{ mb: 1 }} />
                <Typography variant="caption" display="block" color="text.secondary">
                  {agent.personality}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 4 }}>
        <Button
          variant="contained"
          size="large"
          disabled={!theme || selectedAgentIds.length === 0}
          onClick={startGeneration}
          startIcon={<AutoAwesome />}
        >
          Start Magic
        </Button>
      </Box>

      {/* Add Agent Modal */}
      <Dialog open={openAgentModal} onClose={() => setOpenAgentModal(false)}>
        <DialogTitle>Add New Agent</DialogTitle>
        <DialogContent>
          <Stack spacing={3} sx={{ mt: 1, minWidth: 300 }}>
            <TextField
              label="Name" fullWidth
              value={newAgent.name}
              onChange={(e) => setNewAgent({...newAgent, name: e.target.value})}
            />
             <FormControl fullWidth>
              <InputLabel>Role</InputLabel>
              <Select
                value={newAgent.role} label="Role"
                onChange={(e) => setNewAgent({...newAgent, role: e.target.value})}
              >
                <MenuItem value="Host">Host</MenuItem>
                <MenuItem value="Guest">Guest</MenuItem>
                <MenuItem value="Expert">Expert</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Personality" fullWidth multiline rows={2}
              value={newAgent.personality}
              onChange={(e) => setNewAgent({...newAgent, personality: e.target.value})}
            />
            <FormControl fullWidth>
              <InputLabel>Voice</InputLabel>
              <Select
                value={newAgent.voice_id} label="Voice"
                onChange={(e) => setNewAgent({...newAgent, voice_id: e.target.value})}
              >
                {GOOGLE_VOICES.map(voice => (
                  <MenuItem key={voice} value={voice}>{voice}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAgentModal(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleCreateAgent} disabled={!newAgent.name}>Create</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );

  const renderGeneration = () => (
    <Box sx={{ mt: 4, width: '100%' }}>
      <Typography variant="h5" gutterBottom align="center">
        {isGenerating ? 'Cooking up your episode...' : 'Generation Complete'}
      </Typography>

      <LinearProgress variant="determinate" value={progress} sx={{ height: 10, borderRadius: 5, mb: 4 }} />

      <Paper elevation={3} sx={{
        p: 2,
        height: 300,
        overflowY: 'auto',
        bgcolor: '#1e1e1e',
        color: '#00ff00',
        fontFamily: 'monospace'
      }}>
        {logs.map((log, index) => (
          <div key={index}>{log}</div>
        ))}
        <div ref={logsEndRef} />
      </Paper>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button onClick={handleBack} disabled={isGenerating}>Back</Button>
        <Button
          variant="contained"
          disabled={isGenerating || !scriptOutline}
          onClick={handleNext}
        >
          Review Script
        </Button>
      </Box>
    </Box>
  );

  const renderReview = () => (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom>Script Review</Typography>
      {scriptOutline ? (
        <Paper elevation={1} sx={{ p: 4, maxHeight: '60vh', overflowY: 'auto' }}>
          <Typography variant="h6">Topics to Approach</Typography>
          <ul>{scriptOutline.topics_to_approach?.map((t, i) => <li key={i}>{t}</li>)}</ul>

          <Typography variant="h6" sx={{ mt: 2 }}>Topics to Avoid</Typography>
          <ul>{scriptOutline.topics_to_avoid?.map((t, i) => <li key={i}>{t}</li>)}</ul>

          <Typography variant="h6" sx={{ mt: 2 }}>Questions</Typography>
          <ul>{scriptOutline.questions?.map((q, i) => <li key={i}>{q}</li>)}</ul>

          <Typography variant="h6" sx={{ mt: 2 }}>Roles/Structure</Typography>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(scriptOutline.roles, null, 2)}</pre>
        </Paper>
      ) : (
        <Alert severity="error">No script found.</Alert>
      )}

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Button onClick={handleBack}>Back</Button>
        <Button
          variant="contained"
          color="success"
          onClick={handleNext}
          startIcon={<Mic />}
        >
          Go to Studio
        </Button>
      </Box>
    </Box>
  );

  const renderStudio = () => (
    <Box sx={{ mt: 8, textAlign: 'center' }}>
      <Typography variant="h3" gutterBottom>Ready to Record?</Typography>
      <Typography variant="body1" sx={{ mb: 4 }}>
        Your script and agents are ready in the studio.
      </Typography>
      <Button
        variant="contained"
        size="large"
        color="error"
        sx={{ py: 2, px: 6, fontSize: '1.2rem' }}
        onClick={handleEnterStudio}
      >
        Enter Live Studio
      </Button>
    </Box>
  );

  return (
    <Box sx={{ width: '100%', maxWidth: 900, mx: 'auto', p: 4 }}>
      <Stepper activeStep={activeStep}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      <Box sx={{ mt: 2, mb: 1 }}>
        {activeStep === 0 && renderConfig()}
        {activeStep === 1 && renderGeneration()}
        {activeStep === 2 && renderReview()}
        {activeStep === 3 && renderStudio()}
      </Box>
    </Box>
  );
}
