import axios from "axios";

export async function getCurrentUser() {
    try {
        const response = await axios.get("https://mercury.swin.edu.au/cos30043/s104323659/finance-project/backend/session.php");
        return response.data.user || null;
    } catch (error) {
        console.error("Error fetching session:", error);
        return null;
    }
}


export async function logoutUser() {
    await axios.get("https://mercury.swin.edu.au/cos30043/s104323659/finance-project/backend/logout.php");
    localStorage.removeItem("user");
}
