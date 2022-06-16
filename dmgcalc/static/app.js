function dropDownChamp() {
            document.getElementById("dropdownChampionList").classList.toggle("show");
        }

        function chosenChamp(){
            document.getElementById("champion_stats").classList.toggle("show");
            document.getElementById("champion_stats1").classList.toggle("show");
            document.getElementById("champion_stats2").classList.toggle("show");
            document.getElementById("champion_stats3").classList.toggle("show");
            document.getElementById("champion_stats4").classList.toggle("show");
        }

        window.onclick = function (event) {
            if (!event.target.matches(".dropbtn")) {
                var dropdowns = document.getElementsByClassName("dropdown-content")
                var i;
                for (i = 0; i < dropdowns.length; i++) {
                    var openDropdown = dropdowns[i]
                    if (openDropdown.classList.contains('show')) {
                        openDropdown.classList.remove('show')
                    }
                }
            }
        }