async function getCupcakes() {
    try {
        console.log("Fetching cupcakes...");
        const response = await axios.get('/api/cupcakes');
        console.log("API response:", response);

        const cupcakes = response.data.cupcakes;
        console.log("Cupcakes data received:", cupcakes);

        if (Array.isArray(cupcakes)) {
            displayCupcakes(cupcakes);
        } else {
            console.error("Expected an array but got:", cupcakes);
        }
    } catch (error) {
        console.error("Error fetching cupcakes:", error);
    }
}

function displayCupcakes(cupcakes) {
    const cupcakeList = document.getElementById('cupcake-list');
    cupcakeList.innerHTML = ''; // Clear existing cupcakes

    cupcakes.forEach(cupcake => {
        const cupcakeElement = document.createElement('div');
        cupcakeElement.classList.add('card', 'm-3');
        cupcakeElement.style.width = '18rem';

        cupcakeElement.innerHTML = `
            <img src="${cupcake.image}" class="card-img-top" alt="${cupcake.flavor} cupcake">
            <div class="card-body">
                <h5 class="card-title">${cupcake.flavor}</h5>
                <p class="card-text">${cupcake.size} | Rating: ${cupcake.rating}</p>
                <button class="btn btn-danger" onclick="deleteCupcake(${cupcake.id}, this)">Remove</button>
                <button class="btn btn-primary" onclick="editCupcake(${cupcake.id})">Edit</button>
            </div>
        `;

        cupcakeList.appendChild(cupcakeElement);
    });
}



async function deleteCupcake(id, btn) {
    try {
        await axios.delete(`/api/cupcakes/${id}`);
        // Remove cupcake element from the DOM
        btn.closest('.card').remove();
    } catch (error) {
        console.error("Error deleting cupcake:", error);
    }
}

function editCupcake(id) {
    window.location.href = `/edit_cupcake/${id}`;
}



document.addEventListener('DOMContentLoaded', () => {
    getCupcakes();

    document.getElementById("cupcake-form").addEventListener("submit", async (e) => {
        e.preventDefault();

        const flavor = document.getElementById("flavor").value;
        const size = document.getElementById("size").value;
        const rating = document.getElementById("rating").value;
        const image = document.getElementById("image").value || 'https://tinyurl.com/demo-cupcake';

        try {
            const response = await axios.post('/api/cupcakes', {
                flavor,
                size,
                rating,
                image
            });

            const newCupcake = response.data.cupcake;
            addCupcakeToList(newCupcake);

            document.getElementById("cupcake-form").reset();
        } catch (err) {
            console.error(err);
        }
    });
});

function addCupcakeToList(cupcake) {
    const cupcakeList = document.getElementById('cupcake-list');

    const cupcakeElement = document.createElement('div');
    cupcakeElement.classList.add('card', 'm-3');
    cupcakeElement.style.width = '18rem';

    cupcakeElement.innerHTML = `
        <img src="${cupcake.image}" class="card-img-top" alt="${cupcake.flavor} cupcake">
        <div class="card-body">
            <h5 class="card-title">${cupcake.flavor}</h5>
            <p class="card-text">${cupcake.size} | Rating: ${cupcake.rating}</p>
            <button class="btn btn-danger" onclick="deleteCupcake(${cupcake.id}, this)">Remove</button>
            <button class="btn btn-primary" onclick="editCupcake(${cupcake.id})">Edit</button>
        </div>
    `;

    cupcakeList.appendChild(cupcakeElement);
}
