resource "aws_s3_bucket" "bucket" {
  bucket = "container-migration-log"

  tags = {
    Name = "migration_log"
  }
}

resource "aws_s3_bucket_acl" "s3_acl" {
  bucket = aws_s3_bucket.bucket.id
  acl = "private"
}