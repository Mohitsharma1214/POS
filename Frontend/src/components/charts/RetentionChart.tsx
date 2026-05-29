import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

export default function RetentionChart({ data }: { data: number[] }) {
  const chartData = data.map((v, i) => ({ time: i + 1, retention: v }));
  return (
    <div className="w-full h-48 bg-[#23272f] rounded-lg p-4">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <XAxis dataKey="time" stroke="#888" tick={{ fill: '#aaa', fontSize: 12 }} />
          <YAxis stroke="#888" tick={{ fill: '#aaa', fontSize: 12 }} />
          <Tooltip contentStyle={{ background: '#18181b', border: 'none', color: '#fff' }} />
          <Line type="monotone" dataKey="retention" stroke="#6366f1" strokeWidth={3} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
