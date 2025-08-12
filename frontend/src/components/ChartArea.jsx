import React, { useMemo } from 'react'
import { Line } from 'react-chartjs-2'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

export default function ChartArea({ data }) {
  const chartData = useMemo(() => {
    const labels = data.map(d => {
      const dateObj = new Date(d.date)
      return dateObj.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
    })
    const closes = data.map(d => d.close)
    return {
      labels,
      datasets: [
        {
          label: 'Close Price',
          data: closes,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.2,
          pointRadius: 2,
        },
      ],
    }
  }, [data])

  const options = useMemo(() => ({
    responsive: true,
    maintainAspectRatio: false, // allow flexible height
    plugins: {
      legend: {
        position: 'top',
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Date',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Price (USD)',
        },
        beginAtZero: false,
      },
    },
  }), [])

  return (
    <div style={{
      padding: 20,
      minHeight: 320,
      background: '#fff',
      borderRadius: 8,
      boxShadow: '0 1px 6px rgba(0,0,0,0.1)',
      position: 'relative',
      height: '100%',
    }}>
      {data && data.length > 0 ? (
        <Line data={chartData} options={options} />
      ) : (
        <p style={{ color: '#666', textAlign: 'center' }}>No data to display. Select a company.</p>
      )}
    </div>
  )
}
