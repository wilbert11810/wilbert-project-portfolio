<template>
  <div class="container mt-4">
    <h2>Recent Transactions</h2>

    <input v-model="searchQuery" placeholder="Search transactions..." class="form-control mb-3">

    <ul class="list-group">
      <li v-for="transaction in paginatedTransactions" :key="transaction.title" class="list-group-item">
        <h5>{{ transaction.title }} (${{ transaction.amount }})</h5>
        <small class="text-muted">{{ transaction.date }} | {{ transaction.category }}</small>
        <p>{{ transaction.notes }}</p>
      </li>
    </ul>

    <paginate
      :page-count="totalPages"
      :click-handler="changePage"
      :prev-text="'Previous'"
      :next-text="'Next'"
      :container-class="'pagination'"
    />
  </div>
</template>

<script>
import axios from "axios";
import Paginate from "vuejs-paginate-next";

export default {
    components: {
        Paginate,
    },
  data() {
    return {
      transactions: [],
      searchQuery: "",
      currentPage: 1,
      itemsPerPage: 5
    };
  },
  async mounted() {
    await this.fetchTransactions();
  },
  computed: {
    filteredTransactions() {
      return this.transactions.filter(transaction => 
        transaction.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        transaction.category.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        transaction.date.includes(this.searchQuery) ||
        transaction.notes.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    paginatedTransactions() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredTransactions.slice(start, start + this.itemsPerPage);
    },
    totalPages() {
      return Math.ceil(this.filteredTransactions.length / this.itemsPerPage);
    }
  },
  methods: {
    async fetchTransactions() {
      try {
        const response = await axios.get("/cos30043/s104323659/finance-project/expenses.json");
        this.transactions = response.data;
      } catch (error) {
        console.error("Error loading transactions:", error);
      }
    },
    changePage(page) {
      this.currentPage = page;
    }
  }
};
</script>

