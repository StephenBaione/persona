function updateActive(name) {
    document.getElementsByClassName("active")[0].className = "";
    document.getElementById(name).className = "active";
}