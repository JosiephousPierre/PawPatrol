# PAWPATROL Research Prototype

**Hybrid Quantum-Classical Framework for Adaptive Rabies Transmission Modeling and Vaccination Optimization**

A web-based research prototype for simulating rabies transmission across municipalities in Davao de Oro and demonstrating adaptive vaccination recommendations.

## Features

- **Interactive Dashboard** - Overview of simulation data and key metrics
- **Municipality Management** - CRUD operations for municipality data
- **Transmission Simulation** - Day-by-day outbreak simulation engine
- **Adaptive Vaccination** - Rule-based decision recommendations
- **Results Visualization** - Interactive maps and charts
- **Local Storage** - Browser-based data persistence

## Technology Stack

- **Frontend**: Vue 3, Vite, Vue Router, Pinia
- **UI Components**: PrimeVue, Tailwind CSS
- **Visualization**: Leaflet.js, Chart.js
- **Storage**: Browser Local Storage

## Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## Project Structure

```
src/
├── assets/          # Static assets and global styles
├── components/      # Reusable Vue components
├── layouts/         # Application layouts
├── pages/           # Page components
├── router/          # Vue Router configuration
├── services/        # Business logic and utilities
├── stores/          # Pinia state management
└── main.js          # Application entry point
```

## Academic Use

This is a research prototype designed for academic demonstration purposes only. It is not intended for actual public health decision-making.

## License

Academic Research Use Only