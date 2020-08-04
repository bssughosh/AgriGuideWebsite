function check() {
    const states = document.getElementById("states");
    let selected_state = states.options[states.selectedIndex].value;

    window.location.href = '/register/' + selected_state + '/';
}

function check1() {
    const states = document.getElementById("states");
    const dists = document.getElementById("dists");
    let selected_state = states.options[states.selectedIndex].value;
    let selected_dist = dists.options[dists.selectedIndex].value;

    window.location.href = '/register/' + selected_state + '/' + selected_dist + '/';
}