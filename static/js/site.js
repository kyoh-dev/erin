function getMonth() {
    const dateObj = new Date()
    const monthName = dateObj.toLocaleString("default", { month: "long" })
    return {
        month: monthName
    }
}