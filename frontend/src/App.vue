<script setup>
import { onMounted, ref } from "vue";

const getLeaderboard = async () => {
  const response = await fetch(`/api/leaderboard`, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Credentials": true,
    },
  });
  const data = (await response.json()).data;
  data.sort((a, b) => b.score - a.score);
  return data;
};

const leaderboard = ref(null);

onMounted(async () => (leaderboard.value = await getLeaderboard()));

const round = (num) => Math.round((num + Number.EPSILON) * 100) / 100;

const max_scores = [15, 40, 30, 15];
</script>

<template>
  <div class="container mt-4 mb-5">
    <h1 class="mb-4">🏆 NTO ATS Leaderboard</h1>
    <div v-if="leaderboard !== null">
      <table class="table table-sm table-bordered text-center">
        <thead>
          <tr>
            <th colspan="3"></th>
            <th colspan="4">Задачи</th>
            <th></th>
          </tr>
          <tr>
            <th>Место</th>
            <th>Команда</th>
            <th>Баллы</th>
            <th>1</th>
            <th>2</th>
            <th>3</th>
            <th>4</th>
            <th>Участники</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(team, index) of leaderboard">
            <td>{{ index + 1 }}</td>
            <td>{{ team.team }}</td>
            <td>{{ round(team.score) }}</td>
            <td
              v-for="(task, index) of team.task_scores"
              :class="{
                full: task == max_scores[index],
                mid: task != max_scores[index] && task != 0,
                zero: task == 0,
              }"
            >
              {{ round(task) }}
            </td>
            <td class="text-start">
              <ul class="mb-0">
                <li v-for="m in team.members">{{ m }}</li>
              </ul>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="mt-3 text-muted">Лидерборд обновляется каждые 5 минут</div>
      <div>
        Made by
        <a class="link-dark" href="https://github.com/AlanTheKnight"
          >AlanTheKnight</a
        >
        &
        <a class="link-dark" href="https://github.com/zaborshikov"
          >zaborshikov</a
        >
      </div>
    </div>
    <div v-else class="text-center mt-5">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.full {
  background-color: rgb(225, 255, 225);
}

.zero {
  background-color: rgb(255, 225, 225);
}

.mid {
  background-color: rgb(255, 251, 225);
}
</style>
