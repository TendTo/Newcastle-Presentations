FROM haskell:slim

WORKDIR /app

COPY main.hs .

RUN ghc main.hs

ENTRYPOINT ["./main"]
