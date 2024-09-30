
        const countryRegions = {
            "SG": "APAC",
            "HK": "APAC",
            "UAE": "EMEA",
            "UK": "EMEA",
            "USA": "NAM"
        };

        const rootCauseData = {
            "Capacity": ["Unprecedented volume"],
            "Change management": ["Change process not followed", "Impact analysis was not performed"],
            "Code & Configuration": ["Exception handling", "Inadequate / defective configuration"],
            "Access management": ["Entitlement Removed", "Inadequate entitlement"],
            "Security": ["VTM patch", "VTM schedule", "Certificate"],
            "Environment": ["Server/device failure", "High CPU utilization"],
            "User query": ["Functional clarification", "Enhancement request"],
            "System Limitation": ["Insufficient logs", "Technical Limitation"],
            "Data": ["Vendor/external data feed", "Internal data feed"],
            "Batch job": ["NDM connectivity", "Job scheduling"],
            "Third Party": ["Vendor reported issue", "File delayed delivery"],
            "Other": ["Root Cause undetermined", "Insufficient details provided"]
        };

       /*
        function updateRegionDropdown() {
    const countrySelect = document.getElementById("country");
    const regionSelect = document.getElementById("region");
    const selectedCountry = countrySelect.value;

    // Clear previous options
    regionSelect.innerHTML = "";

    // If a country is selected, find the corresponding region
    if (selectedCountry && countryRegions[selectedCountry]) {
        const region = countryRegions[selectedCountry];
        
        // Create and append the region option
        const option = document.createElement("option");
        option.value = region;
        option.text = region;
        regionSelect.appendChild(option);

        // Disable the dropdown to prevent changes
       // regionSelect.disabled = true;
    } 
    

}
*/
function updateRegionDropdown() {
    const countrySelect = document.getElementById("country");
    const regionSelect = document.getElementById("region");
    const selectedCountry = countrySelect.value;

    // Clear previous options
    regionSelect.innerHTML = "";

    // Create the default option
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    defaultOption.text = "Choose Region";
    regionSelect.appendChild(defaultOption);

    // If a country is selected, find the corresponding region
    if (selectedCountry && countryRegions[selectedCountry]) {
        const region = countryRegions[selectedCountry];
        
        // Create and append the region option
        const option = document.createElement("option");
        option.value = region;
        option.text = region;
        regionSelect.appendChild(option);
    } else {
        // If no country is selected, show all regions
        Object.values(countryRegions).forEach(region => {
            const option = document.createElement("option");
            option.value = region;
            option.text = region;
            regionSelect.appendChild(option);
        });
    }
}

// Call this function on page load to show all regions initially
window.onload = function() {
    updateRegionDropdown(); // Populate regions initially
};

/*
        function updateSubCat() {
            const categorySelect = document.getElementById("rootCauseCategory");
            const subcategorySelect = document.getElementById("rootCauseSubCategory");
            const selectedCategory = categorySelect.value;

            subcategorySelect.innerHTML = "";
            if (selectedCategory && rootCauseData[selectedCategory]) {
                const subcategories = rootCauseData[selectedCategory];
                subcategories.forEach(subcategory => {
                    const option = document.createElement("option");
                    option.value = subcategory;
                    option.text = subcategory;
                    subcategorySelect.appendChild(option);
                });
            }
        }
        */window.onload = function() {
    // Populate subcategories with all options initially
    const subcategorySelect = document.getElementById("rootCauseSubCategory");
    for (const category in rootCauseData) {
        rootCauseData[category].forEach(subcategory => {
            const option = document.createElement("option");
            option.value = subcategory;
            option.text = subcategory;
            subcategorySelect.appendChild(option);
        });
    }
};

function updateSubCat() {
    const categorySelect = document.getElementById("rootCauseCategory");
    const subcategorySelect = document.getElementById("rootCauseSubCategory");
    const selectedCategory = categorySelect.value;

    // Clear previous subcategories
    subcategorySelect.innerHTML = "";
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    defaultOption.text = "Root Cause Sub Category";
    subcategorySelect.appendChild(defaultOption);

    if (selectedCategory && rootCauseData[selectedCategory]) {
        const subcategories = rootCauseData[selectedCategory];
        subcategories.forEach(subcategory => {
            const option = document.createElement("option");
            option.value = subcategory;
            option.text = subcategory;
            subcategorySelect.appendChild(option);
        });
    }
}

function displayDescription() {
    const country = document.getElementById('country').value;
    const region = document.getElementById('region').value; // Fixed to get the region value
    const impactedApplication = document.getElementById('impactedApplication').value;
    const causedApplication = document.getElementById('causedApplication').value;
    const rootCauseCategory = document.getElementById('rootCauseCategory').value;
    const rootCauseSubCategory = document.getElementById('rootCauseSubCategory').value;
    const rootCauseAnalysis = document.getElementById('rootCauseAnalysis').value;
    const temporarySolution = document.getElementById('temporarySolution').value;
    const permanentSolution = document.getElementById('permanentSolution').value;
    const recordsChangeNumberProjectNumber = document.getElementById('RecordsChangeNumberProjectNumber').value;
    const businessImpactDetails = document.getElementById('businessImpactDetails').value;
    const preventiveMeasures = document.getElementById('preventiveMeasures').value;

    const description = `
        Impacted Country: ${country}
        Impacted Region: ${region}
        Impacted Application: ${impactedApplication}
        Caused Application: ${causedApplication}
        Root Cause Category: ${rootCauseCategory}
        Root Cause Sub Category: ${rootCauseSubCategory}
        Root Cause Analysis: ${rootCauseAnalysis}
        Temporary Solution: ${temporarySolution}
        Permanent Solution: ${permanentSolution}
        Related records/Change Number/Project number: ${recordsChangeNumberProjectNumber}
        Business Impact Details: ${businessImpactDetails}
        Preventive measures: ${preventiveMeasures}`;

    document.getElementById('descriptionBox').innerText = description;
    document.getElementById('myModal').style.display = "block";
}

function closeModal() {
    document.getElementById('myModal').style.display = "none";
}

function closeConfirmationModal() {
    document.getElementById("confirmationModal").style.display = "none";
}

function copyText() {
    const copyText = document.getElementById("descriptionBox").innerText;
    navigator.clipboard.writeText(copyText).then(() => {
        closeModal();
        document.getElementById("confirmationModal").style.display = "block";
    }).catch(err => {
        console.error('Error copying text: ', err);
    });
}
