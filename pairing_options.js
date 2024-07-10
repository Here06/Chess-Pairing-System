function round_robin() {
    window.location.href = '/round_robin';
}

function Dround_robin() {
    window.location.href = '/dRoundRobin';
}

function swiss() {
    const rounds = prompt("Enter the number of rounds:");
    if (rounds) {
        window.location.href = `/newT?rounds=${rounds}`;
    }
}
