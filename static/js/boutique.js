document.addEventListener('DOMContentLoaded', function() {
    // Validation du formulaire
    const form = document.querySelector('form.needs-validation');
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });

        // Validation de l'image
        const imageInput = document.getElementById('image');
        if (imageInput) {
            imageInput.addEventListener('change', function() {
                const file = this.files[0];
                if (file) {
                    // Vérifier la taille (5MB max)
                    if (file.size > 5 * 1024 * 1024) {
                        this.setCustomValidity('L\'image ne doit pas dépasser 5MB');
                    } else {
                        this.setCustomValidity('');
                    }
                }
            });
        }
    }

    // Gestion du sélecteur de catégorie
    const categorySelect = document.getElementById('category_id');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            if (this.value === '') {
                this.setCustomValidity('Veuillez sélectionner une catégorie');
            } else {
                this.setCustomValidity('');
            }
        });
    }
}); 