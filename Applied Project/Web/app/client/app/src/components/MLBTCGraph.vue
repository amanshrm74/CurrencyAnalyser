<template>
  <section>

    <line-chart :chart-data="chartData" :options="options"></line-chart>

  </section>
</template>

<script>

import LineChart from '../charts/LineChart'
import { HTTP } from '../http-common.js'

export default {
  components: {
    LineChart
  },
  data: () => ({
    chartData: {
      labels: [],
      datasets: []
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  }),
  created () {
    this.fillData()
  },
  methods: {
    fillData () {
      HTTP.get('/currencies/ml/btc/graph')
        .then((response) => {
          this.chartData = response.data
        }, (error) => {
          console.log('ERROR ' + error)
        })
    }
  }
}
</script>

<style>

</style>