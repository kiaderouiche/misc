(require-package 'go-mode)

(defun my-go-mode-hook ()
  ; Use goimports instead of go-fmt
  (let ((goimports (executable-find "goimports")))
    (when goimports
      (setq gofmt-command goimports)))
  ; Call Gofmt before saving
  (add-hook 'before-save-hook 'gofmt-before-save)
  ; Customize compile command to run go build
  (if (not (string-match "go" compile-command))
      (set (make-local-variable 'compile-command)
           "go generate && go build -v && go test -v && go tool vet"))
  ; Go oracle
  ;;(load-file "$GOPATH/src/golang.org/x/tools/cmd/oracle/oracle.el")
  ; Godef jump key binding
  (local-set-key (kbd "M-.") 'godef-jump)
  (local-set-key (kbd "M-*") 'pop-tag-mark)
)
(add-hook 'go-mode-hook 'my-go-mode-hook)
(add-hook 'before-save-hook 'gofmt-before-save)

(require-package 'go-projectile)
(require-package 'golint)
(require-package 'go-gopath)
(require-package 'gotest)

;;AUTO-COMPLETE
(setenv "GOPATH" "/usr/local/go/src/github.com/mdempsky/gocode")
(add-to-list 'exec-path "/usr/local/go/bin/gocode")

;;Load auto-complete
(ac-config-default)
(require 'auto-complete-config)
(require 'go-autocomplete)
;;

(provide 'init-go)


