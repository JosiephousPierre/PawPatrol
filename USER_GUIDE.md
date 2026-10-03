# PAWPATROL User Guide

## Quick Start Guide

### Getting Started

1. **Start the Application**
   ```bash
   npm run dev
   ```
   The application will open at `http://localhost:5173`

2. **Navigate from Landing Page**
   - Click "Explore Dashboard" to enter the application
   - Or click "Learn More" to scroll down and read about the research

---

## Page-by-Page Guide

### 1. 🏠 Landing Page
**Purpose**: Introduction to the PAWPATROL research prototype

**Features**:
- Hero section with project overview
- Research objectives explanation
- Technology stack showcase
- Animated content for engaging presentation

**Actions**:
- Click "Explore Dashboard" → Go to Dashboard
- Click "Learn More" → Scroll to About section
- Click "Get Started" (top right) → Go to Dashboard

---

### 2. 📊 Dashboard Page
**Purpose**: Overview of current system status and statistics

**What You See**:
- **Total Municipalities**: Count of active regions (11)
- **Dog/Cat/Human Population**: Overall population statistics
- **Infected Animals**: Current infection counts (color-coded by severity)
- **Simulation Day**: Current day in simulation
- **Population Distribution Chart**: Pie chart showing species breakdown
- **Risk Level Distribution**: Municipality risk categorization
- **Quick Actions**: Shortcuts to other pages
- **System Status**: Recent activity log

**How to Use**:
1. View summary statistics at a glance
2. Check infection levels (green = safe, red = danger)
3. Use quick action buttons to navigate:
   - "Manage Municipalities" → Municipality Management
   - "Run Simulation" → Simulation Page
   - "View Results" → Results Page

---

### 3. 🗺️ Municipality Management
**Purpose**: Manage the 11 municipalities in Davao de Oro

**Features**:

**Statistics Cards (Top)**:
- Total Municipalities
- High Risk Areas
- Total Dog Population
- Vaccination Coverage

**Data Table**:
- Search bar to find specific municipalities
- Sortable columns (click header to sort)
- Pagination (10 per page)
- Actions: View, Edit, Delete

**How to Use**:

**View a Municipality**:
1. Click the eye icon (👁️) on any row
2. See detailed popup with all information

**Edit a Municipality**:
1. Click the pencil icon (✏️) on any row
2. Modify data in the form
3. Click "Update Municipality"

**Add New Municipality**:
1. Click "Add Municipality" button
2. Fill in the form:
   - Name, coordinates (latitude/longitude)
   - Human/dog/cat populations
   - Initial infected counts
   - Vaccination data
   - Connected municipalities
3. Click "Create Municipality"

**Delete Municipality**:
1. Click trash icon (🗑️) on any row
2. Confirm deletion in popup

**Reset Data**:
1. Click "Reset Data" button
2. Confirm to restore original 11 municipalities

**Search**:
- Type in search box to filter by name or risk level
- Results update instantly

---

### 4. 🧪 Simulation Page
**Purpose**: Configure and run rabies transmission simulations

**Configuration Panel**:

**Basic Settings**:
- **Simulation Days**: How many days to simulate (1-365)
- **Simulation Speed**: 1x, 2x, 5x, or 10x playback speed

**Transmission Parameters**:
- **Base Transmission Rate**: Probability of infection spread (0-1)
- **Environmental Randomness**: Random environmental factors (0-1)

**Vaccination Parameters**:
- **Vaccination Efficiency**: Vaccine effectiveness (0-1)
- **Fractional Alpha**: Fractional-order parameter (0-1)

**Advanced Settings**:
- ☑️ Enable Adaptive Vaccination Decision Module
- ☑️ Enable Detailed Simulation Logs

**How to Run a Simulation**:

1. **Configure Parameters**:
   - Set simulation days (e.g., 30)
   - Choose speed (recommend 5x for testing)
   - Set transmission rate (default: 0.15 = 15%)
   - Set vaccination rate (default: 0.8 = 80%)

2. **Save Configuration**:
   - Click "Save Configuration"
   - Wait for success message

3. **Run Simulation**:
   - Click "Run Simulation"
   - Watch progress bar fill up
   - See day counter increase

4. **Control Simulation**:
   - **Pause**: Freeze simulation
   - **Resume**: Continue from where paused
   - **Stop**: End simulation early
   - **Reset**: Clear all results and start over

5. **View Results**:
   - Click "View Results" button
   - Navigate to Results page

**Information Panel**:
- **Current Configuration**: See active settings
- **Simulation Statistics**: Track progress
- **Quick Actions**: Navigate to related pages

---

### 5. 📈 Results Page
**Purpose**: Visualize simulation outcomes and recommendations

**Summary Statistics (Top)**:
- **Simulation Days**: Total duration
- **Total Infections**: Combined across all species
- **High Risk Areas**: Critical municipalities count
- **Vaccination Coverage**: Overall protection percentage

**Interactive Map**:
- **View**: Davao de Oro region with municipality markers
- **Markers**: Sized by infection level, colored by risk
- **Click Marker**: See popup with details
- **Controls**: Refresh map, toggle fullscreen

**Infection Trends Chart**:
- **X-axis**: Days of simulation
- **Y-axis**: Infection counts
- **Lines**: Separate for dogs, cats, humans
- **Dropdown**: Switch between infection types
  - Infections: Current active cases
  - New Cases: Daily new infections
  - Cumulative: Total over time

**Vaccination Recommendations Table**:
- **Priority**: High, Medium, Low
- **Target Coverage**: Recommended vaccination percentage
- **Infection Rate**: Current infection percentage
- **Reason**: Explanation of recommendation
- **Actions**: Click eye icon to see full details

**Vaccination Coverage Chart**:
- Bar chart showing vaccination % per municipality
- Sorted by coverage level

**Risk Distribution Chart**:
- Pie chart showing municipalities by risk level
- Safe, Low, Moderate, High, Critical

**Simulation Event Log**:
- **Search**: Find specific events
- **Filter**: By severity (info, success, warning, error)
- **Pagination**: 20 entries per page
- **Export**: Download logs as file

**How to Use Results**:

1. **Analyze Overall Impact**:
   - Check summary statistics
   - Note total infections and high-risk areas

2. **Examine Geographic Spread**:
   - Look at map to see affected regions
   - Click markers for municipality details

3. **Review Trends**:
   - Study infection trends chart
   - Identify peaks and patterns

4. **Review Vaccination Strategy**:
   - Check recommendations table
   - Note priority municipalities
   - Read reasons for recommendations

5. **Export Data**:
   - Click "Export Results" for full data
   - Click "Export Logs" for event log
   - Use "New Simulation" to run another

---

### 6. ℹ️ About Page
**Purpose**: Learn about the research methodology and framework

**Sections**:
- Research Overview
- Methodology Explanation
- Framework Components
- Hybrid Quantum-Classical Approach (simulated)
- Technology Stack Details
- Academic Context

**Use Cases**:
- Understanding the research background
- Learning about the framework
- Thesis presentation material

---

## 🎯 Common Workflows

### Workflow 1: First-Time Setup
1. Start at Landing Page
2. Click "Explore Dashboard"
3. Review municipality statistics
4. Click "Manage Municipalities" to see data
5. Return to Dashboard
6. Click "Run Simulation"
7. Configure simulation (keep defaults for first run)
8. Click "Run Simulation"
9. Click "View Results" when done
10. Explore visualizations

### Workflow 2: Modify Municipality & Re-simulate
1. Go to Municipality Management
2. Edit a municipality (increase infected dogs)
3. Go to Simulation Page
4. Run simulation with same settings
5. Go to Results Page
6. Compare with previous results

### Workflow 3: Test Different Parameters
1. Go to Simulation Page
2. Run simulation with low transmission rate (0.10)
3. Note results
4. Reset simulation
5. Run again with high transmission rate (0.25)
6. Compare infection outcomes in Results

### Workflow 4: Analyze Vaccination Strategy
1. Run simulation with adaptive vaccination ON
2. Go to Results Page
3. Review vaccination recommendations
4. Note which municipalities are prioritized
5. Check reasons for recommendations
6. Export recommendations for reference

### Workflow 5: Presentation Mode
1. Start at Landing Page
2. Click "Learn More" to show research objectives
3. Click "Explore Dashboard" to enter app
4. Show Dashboard overview
5. Navigate to Municipalities to show data management
6. Navigate to Simulation to demonstrate configuration
7. Run simulation (use 10x speed for quick demo)
8. Navigate to Results to show visualizations
9. Click municipality markers on map
10. Show vaccination recommendations
11. Navigate to About for research context

---

## 🔧 Tips & Tricks

### Performance Tips
- Use 5x or 10x speed for quick simulations
- Keep simulation days under 100 for faster results
- Clear browser cache if experiencing slowness

### Data Tips
- Use "Reset Data" to restore original municipalities
- Export results before running new simulation
- Save interesting configurations by exporting

### Visualization Tips
- Hover over chart elements for detailed tooltips
- Click map markers for municipality popups
- Use fullscreen mode for better map viewing
- Sort data tables by clicking column headers

### Simulation Tips
- Enable "Detailed Logs" for comprehensive tracking
- Enable "Adaptive Vaccination" for intelligent recommendations
- Start with default parameters for baseline
- Increase transmission rate to simulate worst-case scenarios
- Increase vaccination rate to test prevention strategies

---

## 📱 Mobile Usage

The application is responsive and works on mobile devices:

- **Portrait Mode**: Stack cards vertically
- **Landscape Mode**: Better for charts and maps
- **Touch**: All buttons and controls are touch-friendly
- **Navigation**: Use sidebar menu for page switching

---

## 🐛 Troubleshooting

### Issue: Simulation not starting
**Solution**: 
1. Check all required fields are filled
2. Ensure municipalities have data
3. Try saving configuration first

### Issue: Map not loading
**Solution**:
1. Check internet connection (map tiles load from internet)
2. Refresh the page
3. Try fullscreen mode

### Issue: Data disappeared
**Solution**:
1. Click "Reset Data" to restore defaults
2. Check browser localStorage is enabled
3. Don't use incognito/private mode

### Issue: Charts not displaying
**Solution**:
1. Ensure simulation has been run first
2. Check if there's data to visualize
3. Refresh the page

---

## ⌨️ Keyboard Shortcuts

- **Tab**: Navigate between form fields
- **Enter**: Submit forms
- **Esc**: Close dialogs/popups
- **Arrow Keys**: Navigate dropdown menus

---

## 🎓 For Thesis Presentations

### Recommended Demo Flow:
1. **Introduction** (Landing Page): 30 seconds
2. **Overview** (Dashboard): 1 minute
3. **Data Management** (Municipalities): 1 minute
4. **Configuration** (Simulation): 1 minute
5. **Live Simulation** (Watch it run): 30 seconds
6. **Results Analysis** (Results Page): 2 minutes
7. **Research Context** (About Page): 1 minute

**Total**: ~7 minutes

### Key Points to Highlight:
- ✅ 11 municipalities covered
- ✅ Multi-species transmission modeling
- ✅ 10+ adaptive vaccination rules
- ✅ Real-time interactive visualizations
- ✅ Geographic mapping integration
- ✅ Intelligent decision support
- ✅ Professional UI/UX design

---

## 📞 Support

For technical issues or questions:
1. Check this User Guide
2. Review documentation files in project root
3. Contact research team through academic channels

---

## 🎉 Enjoy Using PAWPATROL!

This research prototype demonstrates advanced concepts in:
- Epidemiological modeling
- Public health optimization
- Disease control strategies
- Data visualization
- Decision support systems

Use it to explore, learn, and demonstrate innovative approaches to rabies control in the Philippines.

---

*Last Updated: 2024*  
*Version: 1.0 - Complete & Thesis-Ready*
