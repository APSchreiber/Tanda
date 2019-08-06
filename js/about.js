$(function () {
    window.tanda = window.tanda || {};
    window.tanda.about = window.tanda.about ||
        {
            aboutText: tandaConfig.aboutText,

            aboutLanguage: "en",
            textCounter: 0,

            // Functions

            setText: function (index) {
                var aboutText = window.tanda.about.aboutText;
                var aboutLanguage = window.tanda.about.aboutLanguage;
                var text = aboutText[index];
                var header = aboutLanguage === "en" ? text.heading : text.heading_es;
                var copy = aboutLanguage === "en" ? text.copy : text.copy_es;
                $("#aboutContent h3").html(header);
                $("#aboutContent p").html(copy);
            },

            textChange: function (direction) {
                var aboutText = window.tanda.about.aboutText;
                if (direction === "back") {
                    if (window.tanda.about.textCounter > 0) {
                        window.tanda.about.textCounter -= 1;
                        window.tanda.about.setText(window.tanda.about.textCounter);
                    }
                }
                else if (direction === "next") {
                    if (window.tanda.about.textCounter < aboutText.length - 1) {
                        window.tanda.about.textCounter += 1;
                        window.tanda.about.setText(window.tanda.about.textCounter);
                    }
                }
                else {
                    window.tanda.about.setText(window.tanda.about.textCounter)
                }
            },

            init: function () {
                window.tanda.about.setText(window.tanda.about.textCounter);

                $(".aboutArrow").click(function () {
                    var arrowClicked = $(this).html();
                    if (arrowClicked == "&lt;") {
                        window.tanda.about.textChange("back")
                    }
                    else {
                        window.tanda.about.textChange("next")
                    }
                });

                $("#languageSelect").on("change", function() {
                    var selectedLanguage = $(this).val();
                    window.tanda.about.aboutLanguage = selectedLanguage;
                    window.tanda.about.textChange();
                });
            }

        }

    window.tanda.about.init();

});