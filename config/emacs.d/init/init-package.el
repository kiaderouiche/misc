(require 'package)

;; (add-to-list 'package-archives
;;              '("melpa" . "http://melpa.milkbox.net/packages/") t)

;;(add-to-list 'package-archives '("melpa" . "http://melpa.org/packages/") t)
;;(add-to-list 'package-archives '("elpa" . "http://elpa.gnu.org/packages/") t)

(setq package-archives '(("melpa" . "https://melpa.org/packages/")
                           ("marmalade" . "https://marmalade-repo.org/packages/")
                           ("org" . "https://orgmode.org/elpa/")
                           ("gnu" . "https://elpa.gnu.org/packages/")
                           ("elpy" . "https://jorgenschaefer.github.io/packages/")))

(defun require-package (package &optional min-version no-refresh)
  "Install given PACKAGE, optionally requiring MIN-VERSION.
If NO-REFRESH is non-nil, the available package lists will not be
re-downloaded in order to locate PACKAGE."
  (if (package-installed-p package min-version)
      t
    (if (or (assoc package package-archive-contents) no-refresh)
        (package-install package)
      (progn
        (package-refresh-contents)
        (require-package package min-version t))))
  (require package))

(defmacro after-load (feature &rest body)
  "After FEATURE is loaded, evaluate BODY."
  (declare (indent defun))
  `(eval-after-load ,feature
     '(progn ,@body)))

(defun add-auto-mode (mode &rest patterns)
  "Add entries to `auto-mode-alist' to use `MODE' for all given file `PATTERNS'."
  (dolist (pattern patterns)
    (add-to-list 'auto-mode-alist (cons pattern mode))))


(setq package-enable-at-startup nil)
(package-initialize)

(require-package 'diminish)

(provide 'init-package)
