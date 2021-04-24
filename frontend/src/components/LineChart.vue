<script>
import { defineComponent } from 'vue'
import { Line } from 'vue3-chart-v2'

export default defineComponent({
  name: 'MonthlyChart',
  extends: Line,
  props: {
    data: [],
    labels: []
  },
  mounted () {
    this.updateChart();
    window.addEventListener("resize", this.updateChart);
  },
  methods: {
    updateChart() {
        console.log("Updating chart.");
        this.renderChart({
              labels: this.labels,
              datasets: this.data
            }, {
            responsive: true,
            maintainAspectRatio: false,
            enableZoom: false,
            scales: {
              yAxes: [{
                gridLines: {
                  display: true,
                  color: "#222",
                  zeroLineColor: '#222'
                },
                ticks: {
                    fontSize: 16
                }
              }],
              xAxes: [{
                gridLines: {
                  display: false,
                  color: "#222",
                  zeroLineColor: '#222'
                },
                ticks: {
                    fontSize: 16
                }
              }]
            },
            legend: {
                labels: {
                    fontSize: 16,
                    usePointStyle: true,
                    pointStyle: "o"
                }
            },
            defaults: {
                font: {
                    size: 20,
                }
            }

        })
    }
  },
  watch: {
    labels: function() {
      this.updateChart();
    },
    data: function() {
      this.updateChart();
    }
  },
  unmounted() {
    window.removeEventListener("resize", this.updateChart);
  },
})
</script>