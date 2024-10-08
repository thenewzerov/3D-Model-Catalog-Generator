function filterTable() {
    let globalInput = document.getElementById("globalFilter").value.toUpperCase();

    let excludes = [];
    let onlys = [];

    // Get all the radio buttons
    const filters = document.querySelectorAll('input[type=radio]');
    for (let i = 0; i < filters.length; i++) {
        if (filters[i].checked) {
            if (filters[i].value === 'exclude') {
                excludes.push(filters[i].name);
            } else if (filters[i].value === 'only') {
                onlys.push(filters[i].name);
            }
        }
    }

    let table = document.getElementById("figuresTable");
    let tbody = table.getElementsByTagName("tbody")[0];
    let tr = tbody.getElementsByTagName("tr");

    for (let i = 0; i < tr.length; i++) {
        const tds = tr[i].getElementsByTagName("td");
        let textMatch = false;

        // Check if the text input matches any of the columns except isMini and isSafe
        for (let j = 0; j < tds.length - 2; j++) {
            if (tds[j]) {
                const txtValue = tds[j].textContent || tds[j].innerText;
                if (txtValue.toUpperCase().indexOf(globalInput) > -1) {
                    textMatch = true;
                    break;
                }
            }
        }

        // Check if the tags column (index 4) matches the filters
        // Look for it not being in the excludes array
        // Or not in the onlys array
        let matchesFilters = false;

        // Get the tags column
        const txtValue = tds[4].textContent || tds[4].innerText;

        // Split the tags into an array
        const tags = txtValue.split(', ');

        // Check if the tags match the filters
        for (let j = 0; j < tags.length; j++) {
            if (!excludes.includes(tags[j])) {
                if (onlys.length === 0 || (onlys.includes(tags[j]))) {
                    matchesFilters = true;
                    break;
                }
            }else{
                break;
            }
        }

        // Apply blur effect if column 4 contains NSFW
        let imgCell = tds[5].getElementsByTagName("img")[0];
        if (tds[4].textContent.toUpperCase().includes("NSFW")) {
            imgCell.classList.add("blurred-image");
        } else {
            imgCell.classList.remove("blurred-image");
        }

        // Show the row if all conditions are met
        if (textMatch && matchesFilters) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }
}

function toggleFilterVisible() {
    filterDiv = document.getElementById("filters");
    if (filterDiv.style.display === "none") {
        filterDiv.style.display = "block";
    } else {
        filterDiv.style.display = "none";
    }
}

function getModelsPerFilter(){
    // Find each label with a type=count and value property
    const labels = document.querySelectorAll('label');

    for (let i = 0; i < labels.length; i++) {
        // See if the label has a type=count and value property
        if (labels[i].getAttribute('type') === 'count' && labels[i].getAttribute('value')) {
            // Get the value of the label
            const value = labels[i].getAttribute('value');

            // Count the rows that have the value in the tags column
            let table = document.getElementById("figuresTable");
            let tbody = table.getElementsByTagName("tbody")[0];
            let tr = tbody.getElementsByTagName("tr");

            let count = 0;
            for (let j = 0; j < tr.length; j++) {
                const tds = tr[j].getElementsByTagName("td");
                const txtValue = tds[4].textContent || tds[4].innerText;
                if (txtValue.includes(value)) {
                    count++;
                }
            }

            // Set the count in the label
            labels[i].textContent = `Total ${value} Models: ${count}`;
        }
    }
}

getModelsPerFilter();
filterTable();
