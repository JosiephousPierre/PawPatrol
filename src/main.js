import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import router from './router'
import App from './App.vue'

// Styles
import './assets/main.css'
import 'primevue/resources/themes/lara-light-blue/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

// PrimeVue Components
import Button from 'primevue/button'
import Card from 'primevue/card'
import Sidebar from 'primevue/sidebar'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Dropdown from 'primevue/dropdown'
import MultiSelect from 'primevue/multiselect'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import Toast from 'primevue/toast'
import ToastService from 'primevue/toastservice'
import ProgressBar from 'primevue/progressbar'
import ConfirmDialog from 'primevue/confirmdialog'
import ConfirmationService from 'primevue/confirmationservice'
import Tooltip from 'primevue/tooltip'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(PrimeVue)
app.use(ToastService)
app.use(ConfirmationService)

// Register PrimeVue components globally
app.component('Button', Button)
app.component('Card', Card)
app.component('Sidebar', Sidebar)
app.component('InputText', InputText)
app.component('InputNumber', InputNumber)
app.component('Dropdown', Dropdown)
app.component('MultiSelect', MultiSelect)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Dialog', Dialog)
app.component('Toast', Toast)
app.component('ProgressBar', ProgressBar)
app.component('ConfirmDialog', ConfirmDialog)

// Register directives
app.directive('tooltip', Tooltip)

app.mount('#app')