document.addEventListener('DOMContentLoaded', () => {
    const players = document.querySelectorAll('.player');
    const numPlayers = players.length;

    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    players.forEach((playerDiv, index) => {
        // const angle = ((360 / numPlayers) * index - 90) * (Math.PI / 180);
        // playerDiv.style.transform = `rotate(${angle}deg)`;
        const playerWidth = playerDiv.offsetWidth;
        const playerHeight = playerDiv.offsetHeight;
        const margin = 100;

        console.log(index);
        var x = 0;
        var y = 0;

        if (index === 0 | index === 1 | index === 9) {
            // This is the bottom
            y = windowHeight - playerHeight - margin;
        } else if (index === 2 | index === 8) {
            // 1st layer above bottom
            y = windowHeight*0.7 - playerHeight;
        } else if (index === 3 | index === 7) {
            // 2nd layer above bottom
            y = windowHeight*0.3 - playerHeight;
        } else if (index === 4 | index === 5 | index === 6) {
            // top
            y = margin;
        }

        if (index === 2 | index === 3) {
            // This is the left edge
            x = margin;
        } else if (index === 1 | index === 4) {
            // 1st layer from left
            x = windowWidth*0.25 - playerWidth/2;
        } else if (index === 0 | index === 5) {
            console.log("found it")
            // 2nd layer from left (center)
            x = windowWidth*0.5 - playerWidth/2;
            console.log(x);
        } else if (index === 6 | index === 9) {
            // 3rd layer from left
            x = windowWidth*0.75 - playerWidth/2;
        } else if (index === 7 | index === 8) {
            // Right edge
            x = windowWidth - playerWidth - margin;
        }
        console.log(x);
        console.log(y);
        // Set the coordinates
        playerDiv.style.left = x + 'px';
        playerDiv.style.top = y + 'px';
    });
});



