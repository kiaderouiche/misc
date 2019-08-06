;;Line editor
(when (version<= "26.0.50" emacs-version )
  (global-display-line-numbers-mode))

(add-to-list 'default-frame-alist
                       '(font . "DejaVu Sans Mono-11"))

(setq-default cursor-type 'bar)

(scroll-bar-mode 1)

(tool-bar-mode 1)

(menu-bar-mode 1)

(blink-cursor-mode -1)

(line-number-mode t)

(column-number-mode t)

(size-indication-mode t)

(fringe-mode 1)

(fset 'yes-or-no-p 'y-or-n-p)

(setq scroll-margin 0)
(setq scroll-conservatively 0)
(setq scroll-preserve-screen-position 1)

;; (global-hl-line-mode -1)
;; Directory Tree
(add-to-list 'load-path "/home/kiad/.emacs.d/snippets/neotree")
(require 'neotree)

(provide 'init-gui)
