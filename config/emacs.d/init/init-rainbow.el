(require-package 'rainbow-mode)
(require-package 'rainbow-delimiters)
(require-package 'zone-rainbow)

(zone-select-add-program 'zone-pgm-rainbow)

(rainbow-mode t)


(add-hook 'prog-mode-hook #'rainbow-delimiters-mode)

(provide 'init-rainbow)
