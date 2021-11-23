
    let repo_id = "{{repo_uuid}}"; // the object that we'll be looking for in the APIs
    let repo_scan_started = "{{repo_scan_started}}";  // If the scan is started, go to long polling api to check when completed. 
    let repo_scan_completed = "{{repo_scan_completed}}";  // If the scan is completed, go to collecting the results
    let scan_id = "{{scan_response_id}}"
    let root_url = window.location.href
    if (root_url.slice(-1)==='/'){
        scan_api_url = window.location.href + `scan_status/${scan_id}`
        result_api_url = window.location.href + `repo_dependencies/${repo_id}`
    }
    else {
        scan_api_url = window.location.href + `/scan_status/${scan_id}`
        result_api_url = window.location.href + `/repo_dependencies/${repo_id}`
    }
    console.log(root_url)
    console.log(scan_api_url)
    console.log(result_api_url)
    let loop_counter = 0
    let continue_marker = 'not'

    async function subscribe(loop_counter) {
        response = await fetch(scan_api_url)
        json = await response.json()
        console.log(json.status)
        console.log(loop_counter)
        if ((json.status == 'complete') || (loop_counter > 100 ))
            return json.status
        else {
            document.getElementById("scan_status").innerHTML = 'Scanning the repo for ' + 3*loop_counter + ' seconds';
            await new Promise(resolve => setTimeout(resolve, 3000));
            loop_counter += 1
            await subscribe(loop_counter);
        }
    }

    async function render() {
        console.log('starting_render')
        response = await fetch(result_api_url)
        a = await response.json()
        console.log(a)
        let scan_status = a.status;
        console.log(a.status)
        if (scan_status == 'true') {
            var count = Object.keys(a.results).length;
            var tableHeader = `<table class=\"table table-borderless table-hover\"><thead><tr><th>Dependency Name </th><th>Dependency Language</th><th>Dependency License</th></tr></thead><tbody>`
            var tableContent = "";
            var tableFooter = "</tbody></table>";

            // Loop through the JSON and output each row in to a string.
            for(i = 0; i < count; i++) {
                tableContent = tableContent + "<tr><td>" + a.results[i].dependency_name + "</td><td>" + a.results[i].dependency_language + "</td><td>" + a.results[i].dependency_license + "</td></tr>";
                }
            // return the table
            document.getElementById("response_table").innerHTML = tableHeader + tableContent + tableFooter;
        }
        else {
            // get the error message
            var results = a.results;
            // render the error message
            document.getElementById("response_table").innerHTML = results;
            };
        }


       async function run() {
           console.log('starting run',repo_scan_started)
           if ((repo_scan_started == 'True') && (scan_id != 'None')) {
                console.log(repo_scan_started)
                continue_marker = await subscribe(loop_counter)
                console.log(continue_marker)
           }
           if (repo_scan_started == 'True') {
            render()
            }
        }


        run()
    //run(repo_scan_started)
    


    // the test code for the poll until condition is met
    // this is just a placeholder. It will eventually be a function that evaluates.