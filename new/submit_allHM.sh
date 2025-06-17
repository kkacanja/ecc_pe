for f in */*HM/submit.sub; do
    echo "Submitting $f"
    condor_submit "$f"
done
