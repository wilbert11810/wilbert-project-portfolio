<template>
    <div class="Title">
        <div class="container mt-4">
            <div class="card border shadow-sm rounded p-4">
                <div class="card-body">
                    <div class="p-2">
                        <h2 class="text-center">Groceries</h2>
                    </div>

                <form @submit.prevent="checkForm" class="expenses-form">
                    <div v-if="errors.length" class="alert alert-danger">
                        <p>Please correct the following error(s):</p>
                    <ul>
                        <li v-for="error in errors" :key="error">{{ error }}</li>
                    </ul>
                    </div>

                    <div class="row mb-3 d-md-flex flex-md-row align-items-md-center">
                        <label for="title" class="col-md-3 col-12">Title:</label>
                    <div class="col-md-9">
                        <input v-model="title" type="text" id="title" name="title" class="form-control" placeholder="(e.g. Groceries, Food)">
                    </div>
                    </div>

                    <div class="row mb-3 d-md-flex flex-md-row align-items-md-center">
                        <label for="amount" class="col-md-3 col-12">Amount: $</label>
                    <div class="col-md-9">
                        <input v-model="amount" type="text" id="amount" name="amount" class="form-control" placeholder="1000">
                    </div>
                    </div>

                    <div class="row mb-3 d-md-flex flex-md-row align-items-md-center">
                        <label for="datepicker" class="col-md-3 col-12">Date of Expenses:</label>
                    <div class="col-md-9">
                        <input v-model="datepicker" type="date" id="datepicker" name="datepicker" class="form-control" :max="maxDate">
                    </div>
                    </div>

                    <div class="row mb-3 d-md-flex flex-md-row align-items-md-center">
                        <label for="type" class="col-md-3 col-12">Category:</label>
                    <div class="col-md-9">
                        <select v-model="type" name="type" id="type" class="form-select">
                        <option value="">Please select an option</option>
                        <option value="food">Food</option>
                        <option value="bills">Bills</option>
                        <option value="entertainment">Entertainment</option>
                        <option value="others">Others</option>
                        </select>
                    </div>
                    </div>

                    <div class="row mb-3 d-md-flex flex-md-row align-items-md-center">
                        <label for="notes" class="col-md-3 col-12">Notes (Optional):</label>
                    <div class="col-md-9">
                        <input v-model="notes" type="text" name="notes" id="notes" class="form-control" placeholder="Notes">
                    </div>
                    </div>

                    <div class="text-center">
                        <button type="submit" class="btn btn-primary w-100">Add Expense</button>
                    </div>
                </form>
                </div>
            </div>

            <div class="container mt-4">
                <div class="card border shadow-sm rounded p-3 mb-4">
                    <h2 class="title-overview">Groceries Overview</h2>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-lg-4 col-md-6 col-sm-12">
                                <label>Title Search:</label>
                                <input type="text" v-model="searchQuery" class="form-control" placeholder="Search by title..." />
                            </div>
                            <div class="col-lg-4 col-md-6 col-sm-12">
                                <label>Sort By:</label>
                                <select v-model="sortBy" class="form-select">
                                    <option value="date">Newest First</option>
                                    <option value="amount">Highest Amount First</option>
                                </select>
                            </div>
                            <div class="col-lg-4 col-md-6 col-sm-12">
                                <label>Filter by Category:</label>
                                <select v-model="filterCategory" class="form-select">
                                    <option value="">All</option>
                                    <option value="food">Food</option>
                                    <option value="bills">Bills</option>
                                    <option value="entertainment">Entertainment</option>
                                    <option value="others">Others</option>
                                </select>
                            </div>
                        </div>

                        <div class="row mt-3">
                            <div class="col-lg-4 col-md-6 col-sm-12">
                                <label>Start Date:</label>
                                <input type="date" v-model="filterStartDate" class="form-control">
                            </div>
                            <div class="col-lg-4 col-md-6 col-sm-12">
                                <label>End Date:</label>
                                <input type="date" v-model="filterEndDate" class="form-control">
                            </div>
                        </div>

                        <div class="row mt-3">
                            <div class="col-12 text-center">
                                <button @click="clearFilters" class="btn btn-secondary w-100">Clear Filters</button>
                            </div>
                        </div>

                    </div>
                </div>
                <div class="border shadow-sm rounded p-3">
                    <table class="table table-striped">
                        <thead class="thead-dark">
                            <tr>
                            <th>Date</th>
                            <th>Title</th>
                            <th>Amount ($)</th>
                            <th>Category</th>
                            <th>Notes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="expense in paginatedExpenses" :key="expense.title" @click="editExpense(expense)">
                            <td>{{ expense.date }}</td>
                            <td>{{ expense.title }}</td>
                            <td>${{ expense.amount }}</td>
                            <td>{{ expense.category }}</td>
                            <td>{{ expense.notes }}</td>
                            </tr>
                        </tbody>
                    </table>
                    <paginate 
                    v-if="totalPages > 1"
                    :page-count="totalPages"
                    :click-handler="fetchTransactions"
                    :prev-text="'Prev'"
                    :next-text="'Next'"
                    :container-class="'pagination'"
                    :page-class="'page-item'"
                    :active-class="'currentPage'">
                    </paginate>
                </div>
                
        </div>
        <div v-if="selectedExpense" class="container mt-4">
            <div class="card border shadow-sm rounded p-3">
                <div class="card-header bg-primary text-white">
                    <h5>Edit Expense</h5>
                </div>
                <div class="card-body">
                <div class="row mb-3">
                    <label for="title" class="col-md-3 col-form-label">Title:</label>
                    <div class="col-md-9">
                    <input v-model="selectedExpense.title" type="text" id="title" class="form-control" placeholder="Title">
                    </div>
                </div>

                <div class="row mb-3">
                    <label for="amount" class="col-md-3 col-form-label">Amount:</label>
                    <div class="col-md-9">
                    <input v-model="selectedExpense.amount" type="number" id="amount" class="form-control" placeholder="Amount">
                    </div>
                </div>

                <div class="row mb-3">
                    <label for="date" class="col-md-3 col-form-label">Date:</label>
                    <div class="col-md-9">
                    <input v-model="selectedExpense.datepicker" type="date" id="date" class="form-control" :max="maxDate">
                    </div>
                </div>

                <div class="row mb-3">
                    <label for="category" class="col-md-3 col-form-label">Category:</label>
                    <div class="col-md-9">
                    <select v-model="selectedExpense.category" id="category" class="form-select">
                        <option value="food">Food</option>
                        <option value="bills">Bills</option>
                        <option value="entertainment">Entertainment</option>
                        <option value="others">Others</option>
                    </select>
                    </div>
                </div>

                <div class="row mb-3">
                    <label for="notes" class="col-md-3 col-form-label">Notes:</label>
                    <div class="col-md-9">
                    <input v-model="selectedExpense.notes" type="text" id="notes" class="form-control" placeholder="Notes">
                    </div>
                </div>

                <div class="text-center">
                    <button @click="updateExpense" class="btn btn-success w-100">Update Expense</button>
                </div>
                </div>
            </div>
            </div>


        </div>
    </div>

</template>

<script>
import Paginate from "vuejs-paginate-next";
import axios from "axios";

export default {
    components: {
        Paginate,
    },
    data() {
        return {
            user: JSON.parse(localStorage.getItem("user") || null ),
            title: "",
            amount: "",
            datepicker: "",
            type: "",
            notes: "",
            errors: [],
            expenses: [],
            totalPages: 0,
            totalRecords: 0,
            currentPage: 1,
            itemsPerPage: 5,
            sortBy: "date",
            filterCategory: "",
            filterStartDate: "",
            filterEndDate: "",
            searchQuery: "",
            selectedExpense: null,
            maxDate: new Date().toISOString().split("T")[0]
        };
    },
    methods: {
        async checkForm() {
            this.errors = [];

            if (!this.title) {
                this.errors.push("Title is required.");
            }
            if (!this.amount || this.amount <= 0) {
                this.errors.push("Amount field is required and should be a positive number.");
            }
            if (!this.datepicker) {
                this.errors.push("Please select a valid date.");
            }
            if (!this.type || this.type === "Please select an option") {
                this.errors.push("Please select an expense category.");
            }

            if (!this.errors.length) {
                const newExpense = {
                    user_id: this.user.id,
                    title: this.title,
                    amount: this.amount,
                    date: this.datepicker,
                    category: this.type,
                    notes: this.notes
                };
                try {
                    const response = await fetch("https://mercury.swin.edu.au/cos30043/s104323659/finance-project/backend/add_transaction.php", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(newExpense),
                    });

                    const data = await response.json();
                    if (data.success) {
                        this.fetchTransactions();
                        this.title = "";
                        this.amount = "";
                        this.datepicker = "";
                        this.type = "";
                        this.notes = "";
                    }
                } catch(error) {
                    console.error("Error saving transaction: ", error)
                }

                
            }
        },
        async fetchTransactions(pageNum = this.currentPage) {
            this.currentPage = pageNum;

            const params = new URLSearchParams({
                page: this.currentPage,
                perPage: this.itemsPerPage,
                sortBy: this.sortBy,
                category: this.filterCategory,
                startDate: this.filterStartDate,
                endDate: this.filterEndDate,
                search: this.searchQuery
            }).toString();

            try {
                const response = await fetch(`https://mercury.swin.edu.au/cos30043/s104323659/finance-project/backend/get_transactions.php?${params}`);
                const data = await response.json();
                this.expenses = data.transactions || [];
                this.totalPages = data.totalPages || 0;
                this.totalRecords = data.totalRecords || 0;
            } catch (error) {
                console.error("Error fetching transactions:", error);
            }
        },
        clearFilters() {
        this.filterCategory = "";
        this.filterStartDate = "";
        this.filterEndDate = "";
        this.searchQuery = "";
        this.sortBy = "date";
        this.currentPage = 1;
        this.fetchTransactions();
        },
        editExpense(expense) {
            this.selectedExpense = {...expense, datepicker: expense.date ? expense.date.split(" ")[0] : "" };
            console.log("Selected Expense:", this.selectedExpense);
        },
        async updateExpense() {
            const formattedDate = this.selectedExpense.datepicker
            ? new Date(this.selectedExpense.datepicker).toISOString().split("T")[0]
            : this.selectedExpense.date.split(" ")[0];
            try {
                const response = await axios.post("https://mercury.swin.edu.au/cos30043/s104323659/finance-project/backend/update_expense.php", {
                    expense_id: this.selectedExpense.id,
                    title: this.selectedExpense.title,
                    amount: this.selectedExpense.amount,
                    category: this.selectedExpense.category,
                    date: formattedDate,
                    notes: this.selectedExpense.notes
                });

                if (response.data.message) {
                    alert("Expense updated successfully!");
                    await this.fetchTransactions();  
                } else {
                    console.error("Update failed:", response.data.error);
                }
            } catch (error) {
                console.error("Update error:", error);
            }
        }
    },
    mounted() {
        this.fetchTransactions();
    },
    computed: {
        paginatedExpenses() {
            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            const endIndex = startIndex + this.itemsPerPage;
            return this.filteredExpenses.slice(startIndex, endIndex);
        },
        filteredExpenses() {
            if (!this.expenses || !Array.isArray(this.expenses)) {
                return []; 
            }
            return this.expenses.filter(expense => {
                const matchesCategory = this.filterCategory ? expense.category === this.filterCategory : true;
                const matchesDate = this.filterStartDate && this.filterEndDate
                ? new Date(expense.date) >= new Date(this.filterStartDate) && new Date(expense.date) <= new Date(this.filterEndDate) : true;
                const matchesSearch = expense.title.toLowerCase().includes(this.searchQuery.toLowerCase());
                return matchesCategory && matchesDate && matchesSearch;
            })
            .sort((a, b) => {
                if (this.sortBy === "amount") {
                    return b.amount - a.amount;
                } else {
                    return new Date(b.date) - new Date(a.date);
                }
            });
        }
    },
    watch: {
        expenses(newExpenses) {
            this.currentPage = 1; 
            localStorage.setItem("expenses", JSON.stringify(newExpenses));
        }
    }

};

</script>

<style>
.display-info {
text-align:center;
}
.expenses-form input, .expenses-form select {
    width: 100%;
    padding: 10px;
    margin: 8px 0;
    border-radius: 6px;
    border: 1px solid #ccc;
}
form {
    padding-bottom: 25px;
}
.display-info-table {
    width: 100%;
    align-items: center;
}
td, th {
    border: 1px solid #ddd;
}
.Title {
padding-top: 80px;
}
.pagination {
  display: flex;
  justify-content: center;
  list-style: none;
  padding: 0;
}

.pagination li {
  display: inline-block;
  margin: 5px;
  background-color: #f4f4f4;
  border: 1px solid #ccc;
  cursor: pointer;
}

.pagination li.currentPage {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}
.pagination li:hover {
    background-color: #0056b3;
}

</style>