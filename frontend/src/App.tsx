import React, { useState, useEffect } from 'react';
import { 
  Activity, Shield, Zap, Truck, AlertTriangle, Wind, 
  Droplets, Cpu, Navigation, Radio, Video, BarChart2, 
  CheckCircle, Globe, Layers, RefreshCw, Power
} from 'lucide-react';

interface SystemMetric {
  id: string;
  name: string;
  status: 'OPTIMAL' | 'WARNING' | 'CRITICAL';
  value: string;
  updatedAt: string;
}

interface PerceptionRecord {
  vehicle_id: string;
  lane_departure_detected: boolean;
  curvature_radius: number;
  collision_risk_score: number;
  fused_objects_count: number;
  timestamp: string;
}

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';
const perceptionIngestUrl = `${apiBaseUrl}/api/v1/perception/telemetry/ingest`;
const perceptionHistoryUrl = `${apiBaseUrl}/api/v1/perception/history/INT-001`;

export default function App() {
  const [activeTab, setActiveTab] = useState<'overview' | 'traffic' | 'environment' | 'utilities' | 'security'>('overview');
  const [systemHealth, setSystemHealth] = useState<number>(99.999);
  const [activeAlertsCount, setActiveAlertsCount] = useState<number>(3);
  const [perceptionRecords, setPerceptionRecords] = useState<PerceptionRecord[]>([]);
  const [perceptionConnected, setPerceptionConnected] = useState(false);
  const [isSendingTestFrame, setIsSendingTestFrame] = useState(false);
  const [metrics, setMetrics] = useState<SystemMetric[]>([
    { id: '1', name: 'Air Quality Index (PM2.5)', status: 'WARNING', value: '38.2 µg/m³', updatedAt: 'Just now' },
    { id: '2', name: 'Emergency Green Wave Preemption', status: 'OPTIMAL', value: '4 Active Corridors', updatedAt: '5s ago' },
    { id: '3', name: 'Substation Grid Utilization', status: 'OPTIMAL', value: '72.4% (Stable)', updatedAt: '12s ago' },
    { id: '4', name: 'Stormwater Basin Water Level', status: 'OPTIMAL', value: '1.45m / 3.2m', updatedAt: '2s ago' },
    { id: '5', name: 'Multi-Region Kubernetes GTM', status: 'OPTIMAL', value: '3 Regions Synced', updatedAt: '1s ago' },
    { id: '6', name: 'Autonomous Drone Nest Fleet', status: 'OPTIMAL', value: '8 Drones Ready', updatedAt: '8s ago' }
  ]);

  // Simulate real-time telemetry polling interval
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemHealth(prev => +(prev + (Math.random() * 0.002 - 0.001)).toFixed(3));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const loadPerceptionHistory = async () => {
      try {
        const response = await fetch(perceptionHistoryUrl);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const body = await response.json() as { records: PerceptionRecord[] };
        setPerceptionRecords(body.records.slice(-12).reverse());
        setPerceptionConnected(true);
      } catch {
        setPerceptionConnected(false);
      }
    };

    loadPerceptionHistory();
    const interval = setInterval(loadPerceptionHistory, 3000);
    return () => clearInterval(interval);
  }, []);

  const sendTestPerceptionFrame = async () => {
    setIsSendingTestFrame(true);
    try {
      const response = await fetch(perceptionIngestUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          intersection_id: 'INT-001',
          vehicle_id: `CMD-${Date.now()}`,
          lane_departure_detected: true,
          curvature_radius: 24.0,
          collision_risk_score: 0.82,
          fused_objects_count: 9,
        }),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      setPerceptionConnected(true);
    } catch {
      setPerceptionConnected(false);
    } finally {
      setIsSendingTestFrame(false);
    }
  };

  const criticalPerceptionAlerts = perceptionRecords.filter(
    record => record.collision_risk_score > 0.75 || record.lane_departure_detected,
  ).length;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Top Navigation Bar */}
      <header className="bg-slate-900 border-b border-slate-800 px-6 py-4 flex items-center justify-between shadow-xl">
        <div className="flex items-center space-x-3">
          <div className="bg-cyan-500/10 p-2 rounded-lg border border-cyan-500/30">
            <Cpu className="w-6 h-6 text-cyan-400 animate-pulse" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-wider text-white">MOVISABIO <span className="text-cyan-400">ENTERPRISE COMMAND CENTER</span></h1>
            <p className="text-xs text-slate-400">Municipal 3D Digital Twin & Autonomous Infrastructure Gateway (Phase 3.1)</p>
          </div>
        </div>

        {/* System Status Indicators */}
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2 bg-slate-800/60 px-3 py-1.5 rounded-full border border-slate-700">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
            <span className="text-xs font-medium text-emerald-400">System SLA: {systemHealth}%</span>
          </div>
          <div className="flex items-center space-x-2 bg-slate-800/60 px-3 py-1.5 rounded-full border border-slate-700">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
            <span className="text-xs font-medium text-amber-300">{activeAlertsCount} Active Alerts</span>
          </div>
          <div className="text-xs text-slate-400 font-mono">
            {new Date().toLocaleUTCString()}
          </div>
        </div>
      </header>

      {/* Main Dashboard Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar Navigation */}
        <aside className="w-64 bg-slate-900/80 border-r border-slate-800 p-4 flex flex-col justify-between">
          <nav className="space-y-2">
            <button 
              onClick={() => setActiveTab('overview')}
              className={`w-full flex items-center space-x-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'overview' ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20' : 'text-slate-300 hover:bg-slate-800'}`}
            >
              <Globe className="w-4 h-4" />
              <span>Digital Twin Overview</span>
            </button>
            <button 
              onClick={() => setActiveTab('traffic')}
              className={`w-full flex items-center space-x-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'traffic' ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20' : 'text-slate-300 hover:bg-slate-800'}`}
            >
              <Navigation className="w-4 h-4" />
              <span>Traffic & Emergency</span>
            </button>
            <button 
              onClick={() => setActiveTab('environment')}
              className={`w-full flex items-center space-x-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'environment' ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20' : 'text-slate-300 hover:bg-slate-800'}`}
            >
              <Wind className="w-4 h-4" />
              <span>Environment & Energy</span>
            </button>
            <button 
              onClick={() => setActiveTab('utilities')}
              className={`w-full flex items-center space-x-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'utilities' ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20' : 'text-slate-300 hover:bg-slate-800'}`}
            >
              <Droplets className="w-4 h-4" />
              <span>Utilities & SCADA</span>
            </button>
            <button 
              onClick={() => setActiveTab('security')}
              className={`w-full flex items-center space-x-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${activeTab === 'security' ? 'bg-cyan-500 text-slate-950 shadow-lg shadow-cyan-500/20' : 'text-slate-300 hover:bg-slate-800'}`}
            >
              <Shield className="w-4 h-4" />
              <span>Security & GTM</span>
            </button>
          </nav>

          <div className="bg-slate-800/40 border border-slate-700/60 rounded-xl p-3 text-xs space-y-2">
            <div className="flex items-center justify-between text-slate-400">
              <span>Redis Cluster</span>
              <span className="text-emerald-400 font-mono">Connected</span>
            </div>
            <div className="flex items-center justify-between text-slate-400">
              <span>Prometheus Exporter</span>
              <span className="text-emerald-400 font-mono">Active (/metrics)</span>
            </div>
          </div>
        </aside>

        {/* Central Content View */}
        <main className="flex-1 bg-slate-950 p-6 overflow-y-auto">
          <div className="max-w-7xl mx-auto space-y-6">
            
            {/* Top Telemetry Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {metrics.map((m) => (
                <div key={m.id} className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg relative overflow-hidden">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{m.name}</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded font-mono ${m.status === 'OPTIMAL' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'}`}>
                      {m.status}
                    </span>
                  </div>
                  <div className="text-2xl font-bold font-mono text-white mb-2">{m.value}</div>
                  <div className="text-xs text-slate-500 flex items-center justify-between">
                    <span>Last synchronized</span>
                    <span className="font-mono">{m.updatedAt}</span>
                  </div>
                </div>
              ))}
            </div>

            <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl">
              <div className="flex items-center justify-between mb-5">
                <div>
                  <h2 className="text-lg font-bold text-white">Autonomous Perception Overlay</h2>
                  <p className="text-xs text-slate-500 mt-1">Intersection INT-001 / recent sensor-fusion frames</p>
                </div>
                <div className="flex items-center gap-3 text-xs font-mono">
                  <span className={perceptionConnected ? 'text-emerald-400' : 'text-amber-400'}>
                    {perceptionConnected ? 'API CONNECTED' : 'API OFFLINE'}
                  </span>
                  <span className="text-amber-300">{criticalPerceptionAlerts} critical</span>
                  <button
                    type="button"
                    onClick={sendTestPerceptionFrame}
                    disabled={isSendingTestFrame}
                    title="Send a test perception frame"
                    className="inline-flex items-center gap-1 rounded-md border border-cyan-500/40 px-2 py-1 text-cyan-300 hover:bg-cyan-500/10 disabled:opacity-50"
                  >
                    <RefreshCw className={`h-3 w-3 ${isSendingTestFrame ? 'animate-spin' : ''}`} />
                    Test frame
                  </button>
                </div>
              </div>
              {perceptionRecords.length === 0 ? (
                <div className="border border-dashed border-slate-700 rounded-lg p-8 text-center text-sm text-slate-500">
                  No perception frames received yet.
                </div>
              ) : (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
                  {perceptionRecords.map(record => {
                    const riskPercent = Math.round(record.collision_risk_score * 100);
                    const isCritical = riskPercent > 75 || record.lane_departure_detected;
                    return (
                      <div key={`${record.vehicle_id}-${record.timestamp}`} className="bg-slate-950 border border-slate-800 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-3">
                          <span className="font-mono text-sm text-cyan-300">{record.vehicle_id}</span>
                          <span className={isCritical ? 'text-red-400 text-xs font-mono' : 'text-emerald-400 text-xs font-mono'}>
                            {isCritical ? 'ATTENTION' : 'MONITORING'}
                          </span>
                        </div>
                        <div className="grid grid-cols-3 gap-3 text-xs">
                          <div><span className="text-slate-500 block">Risk</span><strong className="text-white text-lg">{riskPercent}%</strong></div>
                          <div><span className="text-slate-500 block">Curvature</span><strong className="text-white text-lg">{record.curvature_radius.toFixed(1)}m</strong></div>
                          <div><span className="text-slate-500 block">Objects</span><strong className="text-white text-lg">{record.fused_objects_count}</strong></div>
                        </div>
                        <div className="mt-3 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                          <div className={`h-full ${isCritical ? 'bg-red-500' : 'bg-cyan-400'}`} style={{ width: `${riskPercent}%` }} />
                        </div>
                        {record.lane_departure_detected && <p className="text-xs text-amber-300 mt-2">Lane departure detected</p>}
                      </div>
                    );
                  })}
                </div>
              )}
            </section>

            {/* 3D Digital Twin Spatial Simulation Viewport */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl relative">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <Layers className="w-5 h-5 text-cyan-400" />
                  <h2 className="text-lg font-bold text-white">Live Municipal 3D Digital Twin & Sensor Mesh</h2>
                </div>
                <div className="flex items-center space-x-3">
                  <span className="text-xs bg-slate-800 text-slate-300 px-3 py-1 rounded-md border border-slate-700">FPS: 60.0</span>
                  <span className="text-xs bg-cyan-500/20 text-cyan-400 px-3 py-1 rounded-md border border-cyan-500/30 font-mono">WebGL 2.0 Active</span>
                </div>
              </div>

              {/* Viewport Simulation Box */}
              <div className="w-full h-96 bg-slate-950 rounded-xl border border-slate-800 flex flex-col items-center justify-center relative overflow-hidden">
                <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:16px_16px] opacity-40"></div>
                <div className="z-10 text-center space-y-3">
                  <div className="inline-block bg-cyan-500/10 p-4 rounded-full border border-cyan-500/30 animate-bounce">
                    <Globe className="w-10 h-10 text-cyan-400" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-200">MoviSabio Spatial Rendering Engine</h3>
                  <p className="text-sm text-slate-400 max-w-md mx-auto">
                    Streaming real-time IoT telemetry, VSL speed harmonization layers, and autonomous emergency vehicle green wave corridors.
                  </p>
                </div>
              </div>
            </div>

          </div>
        </main>
      </div>
    </div>
  );
}
